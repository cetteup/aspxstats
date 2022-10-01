import re
from typing import Dict, Optional, Tuple, List
from urllib.parse import urljoin

import requests as requests

from .exceptions import ClientError, InvalidResponseError, Error
from .types import LineType, Dataset, ParseTarget, ResponseValidationMode


class AspxClient:
    base_uri: str
    default_headers: Dict[str, str]
    timeout: float
    response_validation_mode: ResponseValidationMode

    session: requests.Session
    not_found_regex: re.Pattern

    def __init__(
            self,
            base_uri: str,
            default_headers: Dict[str, str],
            timeout: float,
            response_validation_mode: ResponseValidationMode
    ):
        self.base_uri = base_uri
        self.default_headers = default_headers
        self.timeout = timeout
        self.response_validation_mode = response_validation_mode

        self.session = requests.session()
        self.session.headers = default_headers

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()

    def close(self) -> None:
        self.session.close()

    def get_aspx_data(self, endpoint: str, params: Optional[Dict[str, Optional[str]]] = None) -> str:
        """
        Fetch raw, unparsed data from a .aspx endpoint
        :param endpoint: (relative) URL of the endpoint
        :param params: query params to send as part of the request
        :return: raw aspx data as a string
        """
        url = urljoin(self.base_uri, endpoint)
        try:
            response = self.session.get(url, params=params, timeout=self.timeout)

            if response.ok:
                return response.text
            else:
                raise ClientError(f'Failed to fetch ASPX data (HTTP/{response.status_code})')
        except requests.RequestException as e:
            raise ClientError(f'Failed to fetch ASPX data: {e}')

    @staticmethod
    def is_valid_aspx_response(
            raw_data: str,
            validation_mode: ResponseValidationMode = ResponseValidationMode.STRICT
    ) -> Tuple[bool, bool]:
        lines = raw_data.split('\n')
        first_line, last_line = lines[0], lines[-1]

        """
        Last line contains an indicator for the message length (excluding delimiters and excluding the last line)
        $	133	$
        => validate message length matches indicated length
        """
        actual_length = AspxClient.determine_actual_response_length(lines)
        indicated_length = AspxClient.get_indicated_response_length(last_line)

        response_valid = (first_line.strip() == 'O' and
                          (actual_length == indicated_length or validation_mode is ResponseValidationMode.LAX)
                          and AspxClient.are_response_datasets_valid(raw_data))

        """
        Each project handles player not found errors a little different
        BF2Hub returns "E\t998" in the first line (all endpoints)
        PlayBF2 returns a converged list of headers and dummy values in the first line (getplayerinfo)
        PlayBF2 returns a line containing "player [...] not found" (getmapinfo [unofficial])
        """
        not_found_error = not response_valid and (
                first_line == 'E\t998'
                or first_line.startswith('O	H	asof	D')
                or next((True for line in lines if 'player' in line.casefold() and 'not found' in line.casefold()), False)
        )

        return response_valid, not_found_error

    @staticmethod
    def determine_actual_response_length(lines: List[str]) -> int:
        """
        Determine the actual response length by counting the non-delimited characters
        :param lines: complete aspx response split into lines
        :return: actual length of the response
        """
        # Ignore the last line, since it should contain the length indicator
        return sum(len(line.replace('\t', '')) for line in lines[:-1])

    @staticmethod
    def get_indicated_response_length(indicator_line: str) -> int:
        """
        Get the indicated response length from the indicator line (last line) of the aspx response
        :param indicator_line: line containing response length indicator "$	14	$" (last line of response)
        :return: indicated length of the response (-1 in case the line does not contain a valid/parseable indicator)
        """
        if not indicator_line.startswith('$\t') or not indicator_line.endswith('\t$'):
            return -1

        try:
            return int(indicator_line.strip('\t$'))
        except ValueError:
            return -1

    @staticmethod
    def are_response_datasets_valid(raw_data: str) -> bool:
        datasets = AspxClient.extract_datasets_from_response(raw_data)
        return all(AspxClient.is_valid_dataset(dataset) for dataset in datasets)

    @staticmethod
    def is_valid_dataset(dataset: Dataset) -> bool:
        """
        Ensure that all value lines of a dataset have the same number of columns as the key line
        :param dataset: dataset to test
        :return: True, if column numbers match, else False
        """
        key_columns = dataset.keys.count('\t')
        return all(value_line.count('\t') == key_columns for value_line in dataset.data)

    @staticmethod
    def parse_aspx_response(raw_data: str, targets: List[ParseTarget]) -> dict:
        """
        Parse raw aspx data into a dictionary
        :param raw_data: raw aspx data as a string
        :param targets: targets to parse data into (defines how datasets in response are added to dictionary structure)
        :return: aspx data as dictionary (structure varies based on endpoint/targets parameter)
        """
        datasets = AspxClient.extract_datasets_from_response(raw_data)

        """
        For most endpoints we get two datasets: one containing metadata and one containing results.
        A common breach of this design: PlayBF2 does not support the rising star leaderboard. If you request it anyway,
        you get a single, empty dataset (which we cannot sensibly parse into the usual leaderboard response format):
        O
        H    size    asof
        $    10    $
        => raise an error if we have fewer dataset than targets to parse to
        """
        if len(datasets) < len(targets):
            raise InvalidResponseError('Received invalid number of datasets from list endpoint')

        return AspxClient.build_dict_from_datasets(datasets, targets)

    @staticmethod
    def extract_datasets_from_response(raw_data: str) -> List[Dataset]:
        lines = raw_data.split('\n')
        datasets: List[Dataset] = []
        # We should see a header line first (since we skip the "status" line)
        current_line_type: LineType = LineType.HEADERS
        data_line_index = 0
        for line in lines[1:]:
            if line[:2] == 'H\t':
                # Line starts with header marker => create and append new dataset
                current_line_type = LineType.HEADERS
                datasets.append(Dataset(line[2:]))
            elif line[:2] == 'D\t':
                # Line starts with data marker => add data line to current dataset
                if current_line_type is LineType.DATA:
                    # Data row is followed by another data row
                    # => increase data line index to add another data line to current dataset
                    # (relevant for player search results for example)
                    data_line_index += 1

                current_line_type = LineType.DATA
                datasets[-1].data.append(line[2:])
            elif line[:2] == '$\t':
                # Line starts with end marker => and stop parsing
                break
            elif current_line_type is LineType.HEADERS:
                # Line has no marker and last marker indicated a header line
                # => append line to header of current dataset
                datasets[-1].keys += line
            else:
                # Line has no marker and last marker indicated a header line
                # => append line to data of current dataset
                datasets[-1].data[data_line_index] += line

        return datasets

    @staticmethod
    def build_dict_from_datasets(datasets: List[Dataset], targets: List[ParseTarget]) -> dict:
        data = {}
        for index, dataset in enumerate(datasets):
            target = targets[index] if index < len(targets) else None
            if target is None:
                # Ever reaching this means we did not receive enough targets to handle all datasets,
                # which would usually be an implementation error
                raise Error('No parse target for aspx response dataset')

            # Split keys/headers into list
            keys = dataset.keys.split('\t')
            # Split each data line into a list
            data_lines = [line.split('\t') for line in dataset.data]

            if target.to_root:
                # Add dataset to dict root
                data.update({key: data_lines[0][index] for (index, key) in enumerate(keys)})
            elif len(data_lines) == 1 and not target.as_list:
                # Only a single line of data, add as properties under key (child object)
                # exception: player search returning only a single player (in that case, force return an array)
                data[target.to_key] = {
                    key: data_lines[0][index] if index < len(data_lines[0]) else ''
                    for (index, key) in enumerate(keys)
                }
            elif target.as_list:
                # Multiple lines of data, create list of dicts
                data[target.to_key] = [
                    {keys[index]: value for (index, value) in enumerate(data_line)}
                    for (index, data_line) in enumerate(data_lines)
                ]

        return data
