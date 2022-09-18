from typing import Optional
from unittest import TestCase
from unittest.mock import patch

import requests

from aspxstats.client import AspxClient, ParseTarget
from aspxstats.exceptions import Error, ClientError, InvalidResponseError


class MockResponse:
    text: str
    status_code: int
    ok: bool

    def __init__(self, text: str, status_code: int, ok: bool):
        self.text = text
        self.status_code = status_code
        self.ok = ok


class MockSession:
    response: MockResponse
    exception: Optional[Exception]

    def __init__(self, response: MockResponse, exception: Optional[Exception] = None):
        self.response = response
        self.exception = exception

    def get(self, *args, **kwargs):
        if self.exception is not None:
            raise self.exception
        else:
            return self.response


class AspxClientTest(TestCase):
    def test_get_aspx_data(self):
        with patch('requests.session') as patched_session:
            # GIVEN
            response_text = 'O\n' \
                            'H\tasof\n' \
                            'D\t1663441990\n' \
                            'H\tpid\tnick\tmtm-0\tmwn-0\tmls-0\n' \
                            'D\t500362798\tmister249\t123\t456\t789\n' \
                            '$\t68\t$'
            patched_session.return_value = MockSession(MockResponse(response_text, 200, True))

            client = AspxClient(
                'http://official.ranking.bf2hub.com/ASP/',
                {
                    'User-Agent': 'GameSpyHTTP/1.0'
                },
                1.0
            )

            # WHEN
            response = client.get_aspx_data('getplayerinfo.aspx', {
                'pid': '500362798',
                'info': 'mtm-0,mwn-0,mls-0'
            })

            # THEN
            self.assertEqual(response_text, response)

    def test_get_aspx_data_error_for_not_ok(self):
        with patch('requests.session') as patched_session:
            # GIVEN
            response_text = 'O\n' \
                            'H\tasof\n' \
                            'D\t1663441990\n' \
                            'H\tpid\tnick\tmtm-0\tmwn-0\tmls-0\n' \
                            'D\t500362798\tmister249\t123\t456\t789\n' \
                            '$\t68\t$'
            patched_session.return_value = MockSession(MockResponse(response_text, 500, False))

            client = AspxClient(
                'http://official.ranking.bf2hub.com/ASP/',
                {
                    'User-Agent': 'GameSpyHTTP/1.0'
                },
                1.0
            )

            # WHEN/THEN
            self.assertRaisesRegex(ClientError, r'^Failed to fetch ASPX data \(HTTP/500\)$', client.get_aspx_data,'getplayerinfo.aspx', {
                'pid': '500362798',
                'info': 'mtm-0,mwn-0,mls-0'
            })

    def test_get_aspx_data_error_for_requests_exception(self):
        with patch('requests.session') as patched_session:
            # GIVEN
            response_text = 'O\n' \
                            'H\tasof\n' \
                            'D\t1663441990\n' \
                            'H\tpid\tnick\tmtm-0\tmwn-0\tmls-0\n' \
                            'D\t500362798\tmister249\t123\t456\t789\n' \
                            '$\t68\t$'
            patched_session.return_value = MockSession(
                MockResponse(response_text, 500, False),
                requests.RequestException('some-error')
            )

            client = AspxClient(
                'http://official.ranking.bf2hub.com/ASP/',
                {
                    'User-Agent': 'GameSpyHTTP/1.0'
                },
                1.0
            )

            # WHEN/THEN
            self.assertRaisesRegex(ClientError, r'^Failed to fetch ASPX data: some-error$', client.get_aspx_data, 'getplayerinfo.aspx', {
                'pid': '500362798',
                'info': 'mtm-0,mwn-0,mls-0'
            })

    def test_is_valid_aspx_response_bf2hub_incorrect_parameters(self):
        # GIVEN
        raw_data = 'E\t216\n' \
                   '$\t4\t$'

        # WHEN
        valid, not_found = AspxClient.is_valid_aspx_response(raw_data)

        # THEN
        self.assertFalse(valid)
        self.assertFalse(not_found)

    def test_is_valid_aspx_response_playbf2_incorrect_parameters_getplayerinfo(self):
        # GIVEN
        raw_data = 'E\n' \
                   'H\tasof\terr\n' \
                   'D\t1663496484\tInvalid Syntax!\n' \
                   '$\t35\t$'

        # WHEN
        valid, not_found = AspxClient.is_valid_aspx_response(raw_data)

        # THEN
        self.assertFalse(valid)
        self.assertFalse(not_found)

    def test_is_valid_aspx_response_playbf2_incorrect_parameters_getleaderboard(self):
        # GIVEN
        raw_data = 'Invalid Syntax!'

        # WHEN
        valid, not_found = AspxClient.is_valid_aspx_response(raw_data)

        # THEN
        self.assertFalse(valid)
        self.assertFalse(not_found)

    def test_is_valid_aspx_response_bf2hub_not_found(self):
        # GIVEN
        raw_data = 'E\t998\n' \
                   '$\t4\t$'

        # WHEN
        valid, not_found = AspxClient.is_valid_aspx_response(raw_data)

        # THEN
        self.assertFalse(valid)
        self.assertTrue(not_found)

    def test_is_valid_aspx_response_playbf2_not_found_getplayerinfo(self):
        # GIVEN
        raw_data = 'O\tH\tasof\tD\t1663441143\tH\tpid\tnick\tscor\tjond\twins\tloss\tmode0\tmode1\tmode2\ttime\tsmoc'

        # WHEN
        valid, not_found = AspxClient.is_valid_aspx_response(raw_data)

        # THEN
        self.assertFalse(valid)
        self.assertTrue(not_found)

    def test_is_valid_aspx_response_playbf2_not_found_unofficial_getmapinfo(self):
        # GIVEN
        raw_data = 'E\n' \
                   'H\terr\n' \
                   'D\tPlayer Map Data Not Found!\n' \
                   '$\t32\t$'

        # WHEN
        valid, not_found = AspxClient.is_valid_aspx_response(raw_data)

        # THEN
        self.assertFalse(valid)
        self.assertTrue(not_found)

    def test_determine_actual_response_length(self):
        # GIVEN
        lines = [
            '1\t2\t3',
            '4\t5\t6',
            '7\t8\t9',
            'ignore-this-line'
        ]

        # WHEN
        actual_length = AspxClient.determine_actual_response_length(lines)

        # THEN
        expected_length = 9
        self.assertEqual(expected_length, actual_length)

    def test_get_indicated_response_length(self):
        # GIVEN
        indicator_line = '$\t68\t$'

        # WHEN
        indicated_length = AspxClient.get_indicated_response_length(indicator_line)

        # THEN
        expected_length = 68
        self.assertEqual(expected_length, indicated_length)

    def test_get_indicated_response_length_invalid_prefix_missing(self):
        # GIVEN
        indicator_line = '68\t$'

        # WHEN
        indicated_length = AspxClient.get_indicated_response_length(indicator_line)

        # THEN
        expected_length = -1
        self.assertEqual(expected_length, indicated_length)

    def test_get_indicated_response_length_invalid_suffix_missing(self):
        # GIVEN
        indicator_line = '$\t68'

        # WHEN
        indicated_length = AspxClient.get_indicated_response_length(indicator_line)

        # THEN
        expected_length = -1
        self.assertEqual(expected_length, indicated_length)

    def test_get_indicated_response_length_invalid_non_int_indicator(self):
        # GIVEN
        indicator_line = '$\tnot-an-integer\t$'

        # WHEN
        indicated_length = AspxClient.get_indicated_response_length(indicator_line)

        # THEN
        expected_length = -1
        self.assertEqual(expected_length, indicated_length)

    def test_parse_aspx_data_getplayerinfo(self):
        # GIVEN
        raw_data = 'O\n' \
                   'H\tasof\n' \
                   'D\t1663441990\n' \
                   'H\tpid\tnick\tmtm-0\tmwn-0\tmls-0\n' \
                   'D\t500362798\tmister249\t123\t456\t789\n' \
                   '$\t68\t$'
        valid, _ = AspxClient.is_valid_aspx_response(raw_data)
        self.assertTrue(valid)

        # WHEN
        parsed = AspxClient.parse_aspx_response(raw_data, [
            ParseTarget(to_root=True),
            ParseTarget('player')
        ])

        # THEN
        expected = {
            'asof': '1663441990',
            'player': {
                'pid': '500362798',
                'nick': 'mister249',
                'mtm-0': '123',
                'mwn-0': '456',
                'mls-0': '789'
            }
        }
        self.assertDictEqual(expected, parsed)

    def test_parse_aspx_data_getrankinfo(self):
        # GIVEN
        raw_data = 'O\n' \
                   'H\trank\tchng\tdecr\n' \
                   'D\t13\t0\t0\n' \
                   '$\t19\t$'
        valid, _ = AspxClient.is_valid_aspx_response(raw_data)
        self.assertTrue(valid)

        # WHEN
        parsed = AspxClient.parse_aspx_response(raw_data, [
            ParseTarget(to_root=True)
        ])

        # THEN
        expected = {
            'rank': '13',
            'chng': '0',
            'decr': '0'
        }
        self.assertDictEqual(expected, parsed)

    def test_parse_aspx_data_getawardsinfo(self):
        # GIVEN
        raw_data = 'O\n' \
                   'H\tpid\tasof\n' \
                   'D\t500362798\t1663097863\n' \
                   'H\taward\tlevel\twhen\tfirst\n' \
                   'D\t1031105\t1\t1601663082\t0\n' \
                   'D\t1031105\t2\t1651345901\t0\n' \
                   '$\t89\t$'
        valid, _ = AspxClient.is_valid_aspx_response(raw_data)
        self.assertTrue(valid)

        # WHEN
        parsed = AspxClient.parse_aspx_response(raw_data, [
            ParseTarget(to_root=True),
            ParseTarget('awards', as_list=True)
        ])

        # THEN
        expected = {
            'pid': '500362798',
            'asof': '1663097863',
            'awards': [
                {
                    'award': '1031105',
                    'level': '1',
                    'when': '1601663082',
                    'first': '0'
                },
                {
                    'award': '1031105',
                    'level': '2',
                    'when': '1651345901',
                    'first': '0'
                }
            ]
        }
        self.assertDictEqual(expected, parsed)

    def test_parse_aspx_data_getawardsinfo_no_awards(self):
        # GIVEN
        raw_data = 'O\n' \
                   'H\tpid\tasof\n' \
                   'D\t500362798\t1663097863\n' \
                   'H\taward\tlevel\twhen\tfirst\n' \
                   '$\t49\t$'
        valid, _ = AspxClient.is_valid_aspx_response(raw_data)
        self.assertTrue(valid)

        # WHEN
        parsed = AspxClient.parse_aspx_response(raw_data, [
            ParseTarget(to_root=True),
            ParseTarget('awards', as_list=True)
        ])

        # THEN
        expected = {
            'pid': '500362798',
            'asof': '1663097863',
            'awards': []
        }
        self.assertDictEqual(expected, parsed)

    def test_parse_aspx_data_getunlocksinfo(self):
        # GIVEN
        raw_data = 'O\n' \
                   'H\tpid\tnick\tasof\n' \
                   'D\t500362798\tmister249\t1663441990\n' \
                   'H\tenlisted\tofficer\n' \
                   'D\t0\t0\n' \
                   'H\tid\tstate\n' \
                   'D\t11\ts\n' \
                   'D\t22\ts\n' \
                   '$\t77\t$'
        valid, _ = AspxClient.is_valid_aspx_response(raw_data)
        self.assertTrue(valid)

        # WHEN
        parsed = AspxClient.parse_aspx_response(raw_data, [
            ParseTarget(to_root=True),
            ParseTarget('status'),
            ParseTarget('unlocks', as_list=True)
        ])

        # THEN
        expected = {
            'pid': '500362798',
            'nick': 'mister249',
            'asof': '1663441990',
            'status': {
                'enlisted': '0',
                'officer': '0'
            },
            'unlocks': [
                {
                    "id": "11",
                    "state": "s"
                },
                {
                    "id": "22",
                    "state": "s"
                },
            ]
        }
        self.assertDictEqual(expected, parsed)

    def test_parse_aspx_data_getleaderboard(self):
        # GIVEN
        raw_data = 'O\n' \
                   'H\tsize\tasof\n' \
                   'D\t100000\t1663365600\n' \
                   'H\tn\tpid\tnick\tscore\ttotaltime\tplayerrank\tcountrycode\n' \
                   'D\t1\t43812139\tThe_Man_13\t2768530\t45548584\t21\tUS\n' \
                   'D\t2\t75474155\tJAAPIO_DE_SLACHTER\t2471428\t49817187\t21\tAL\n' \
                   '$\t157\t$'
        valid, _ = AspxClient.is_valid_aspx_response(raw_data)
        self.assertTrue(valid)

        # WHEN
        parsed = AspxClient.parse_aspx_response(raw_data, [
            ParseTarget(to_root=True),
            ParseTarget('players', as_list=True)
        ])

        # THEN
        expected = {
            'size': '100000',
            'asof': '1663365600',
            'players': [
                {
                    'n': '1',
                    'pid': '43812139',
                    'nick': 'The_Man_13',
                    'score': '2768530',
                    'totaltime': '45548584',
                    'playerrank': '21',
                    'countrycode': 'US'
                },
                {
                    'n': '2',
                    'pid': '75474155',
                    'nick': 'JAAPIO_DE_SLACHTER',
                    'score': '2471428',
                    'totaltime': '49817187',
                    'playerrank': '21',
                    'countrycode': 'AL'
                }
            ]
        }
        self.assertDictEqual(expected, parsed)

    def test_parse_aspx_data_getleaderboard_no_results(self):
        # GIVEN
        raw_data = 'O\n' \
                   'H\tsize\tasof\n' \
                   'D\t100000\t1663365600\n' \
                   'H\tn\tpid\tnick\tscore\ttotaltime\tplayerrank\tcountrycode\n' \
                   '$\t71\t$'
        valid, _ = AspxClient.is_valid_aspx_response(raw_data)
        self.assertTrue(valid)

        # WHEN
        parsed = AspxClient.parse_aspx_response(raw_data, [
            ParseTarget(to_root=True),
            ParseTarget('players', as_list=True)
        ])

        # THEN
        expected = {
            'size': '100000',
            'asof': '1663365600',
            'players': []
        }
        self.assertDictEqual(expected, parsed)

    def test_parse_aspx_data_searchforplayers(self):
        # GIVEN
        raw_data = 'O\n' \
                   'H\tasof\n' \
                   'D\t1663447766\n' \
                   'H\tn\tpid\tnick\tscore\n' \
                   'D\t1\t45377286\tmister24\t6458\n' \
                   'D\t2\t500362798\tmister249\t86136\n' \
                   '$\t78\t$'
        valid, _ = AspxClient.is_valid_aspx_response(raw_data)
        self.assertTrue(valid)

        # WHEN
        parsed = AspxClient.parse_aspx_response(raw_data, [
            ParseTarget(to_root=True),
            ParseTarget('players', as_list=True)
        ])

        # THEN
        expected = {
            'asof': '1663447766',
            'players': [
                {
                    'n': '1',
                    'pid': '45377286',
                    'nick': 'mister24',
                    'score': '6458'
                },
                {
                    'n': '2',
                    'pid': '500362798',
                    'nick': 'mister249',
                    'score': '86136'
                }
            ]
        }
        self.assertDictEqual(expected, parsed)

    def test_parse_aspx_data_searchforplayers_single_result(self):
        # GIVEN
        raw_data = 'O\n' \
                   'H\tasof\n' \
                   'D\t1663447766\n' \
                   'H\tn\tpid\tnick\tscore\n' \
                   'D\t1\t500362798\tmister249\t86136\n' \
                   '$\t56\t$'
        valid, _ = AspxClient.is_valid_aspx_response(raw_data)
        self.assertTrue(valid)

        # WHEN
        parsed = AspxClient.parse_aspx_response(raw_data, [
            ParseTarget(to_root=True),
            ParseTarget('players', as_list=True)
        ])

        # THEN
        expected = {
            'asof': '1663447766',
            'players': [
                {
                    'n': '1',
                    'pid': '500362798',
                    'nick': 'mister249',
                    'score': '86136'
                }
            ]
        }
        self.assertDictEqual(expected, parsed)

    def test_parse_aspx_data_searchforplayers_no_results(self):
        # GIVEN
        raw_data = 'O\n' \
                   'H\tasof\n' \
                   'D\t1663447766\n' \
                   'H\tn\tpid\tnick\tscore\n' \
                   '$\t31\t$'
        valid, _ = AspxClient.is_valid_aspx_response(raw_data)
        self.assertTrue(valid)

        # WHEN
        parsed = AspxClient.parse_aspx_response(raw_data, [
            ParseTarget(to_root=True),
            ParseTarget('players', as_list=True)
        ])

        # THEN
        expected = {
            'asof': '1663447766',
            'players': []
        }
        self.assertDictEqual(expected, parsed)

    def test_parse_aspx_data_getbackendinfo(self):
        # GIVEN
        raw_data = 'O\n' \
                   'H\tver\tnow\n' \
                   'D\t0.1\t1663494349\n' \
                   'H\tid\tkit\tname\tdescr\n' \
                   'D\t11\t0\tChsht_protecta\tProtecta shotgun with slugs\n' \
                   'D\t22\t1\tUsrif_g3a3\tH&K G3\n' \
                   '$\t102\t$'
        valid, _ = AspxClient.is_valid_aspx_response(raw_data)
        self.assertTrue(valid)

        # WHEN
        parsed = AspxClient.parse_aspx_response(raw_data, [
            ParseTarget(to_root=True),
            ParseTarget('unlocks', as_list=True)
        ])

        # THEN
        expected = {
            'ver': '0.1',
            'now': '1663494349',
            'unlocks': [
                {
                    'id': '11',
                    'kit': '0',
                    'name': 'Chsht_protecta',
                    'descr': 'Protecta shotgun with slugs'
                },
                {
                    'id': '22',
                    'kit': '1',
                    'name': 'Usrif_g3a3',
                    'descr': 'H&K G3'
                }
            ]
        }
        self.assertDictEqual(expected, parsed)

    def test_parse_aspx_data_unofficial_getmapinfo(self):
        # GIVEN
        raw_data = 'O\n' \
                   'H\tmapid\tname\tscore\ttime\ttimes\tkills\tdeaths\n' \
                   'D\t0\tkubra_dam\t5938461\t15647665\t8115\t1825256\t2177517\n' \
                   'D\t1\tmashtuur_city\t7452370\t18121386\t15777\t2180707\t2203487\n' \
                   '$\t129\t$'
        valid, _ = AspxClient.is_valid_aspx_response(raw_data)
        self.assertTrue(valid)

        # WHEN
        parsed = AspxClient.parse_aspx_response(raw_data, [
            ParseTarget('maps', as_list=True)
        ])

        # THEN
        expected = {
            'maps': [
                {
                    'mapid': '0',
                    'name': 'kubra_dam',
                    'score': '5938461',
                    'time': '15647665',
                    'times': '8115',
                    'kills': '1825256',
                    'deaths': '2177517'
                },
                {
                    'mapid': '1',
                    'name': 'mashtuur_city',
                    'score': '7452370',
                    'time': '18121386',
                    'times': '15777',
                    'kills': '2180707',
                    'deaths': '2203487'
                }
            ]
        }
        self.assertDictEqual(expected, parsed)

    def test_parse_aspx_data_unofficial_getmapinfo_single_result(self):
        # GIVEN
        raw_data = 'O\n' \
                   'H\tmapid\tname\tscore\ttime\ttimes\tkills\tdeaths\n' \
                   'D\t0\tkubra_dam\t5938461\t15647665\t8115\t1825256\t2177517\n' \
                   '$\t80\t$'
        valid, _ = AspxClient.is_valid_aspx_response(raw_data)
        self.assertTrue(valid)

        # WHEN
        parsed = AspxClient.parse_aspx_response(raw_data, [
            ParseTarget('maps', as_list=True)
        ])

        # THEN
        expected = {
            'maps': [
                {
                    'mapid': '0',
                    'name': 'kubra_dam',
                    'score': '5938461',
                    'time': '15647665',
                    'times': '8115',
                    'kills': '1825256',
                    'deaths': '2177517'
                }
            ]
        }
        self.assertDictEqual(expected, parsed)

    def test_parse_aspx_data_unofficial_getmapinfo_no_results(self):
        # GIVEN
        raw_data = 'O\n' \
                   'H\tmapid\tname\tscore\ttime\ttimes\tkills\tdeaths\n' \
                   '$\t36\t$'
        valid, _ = AspxClient.is_valid_aspx_response(raw_data)
        self.assertTrue(valid)

        # WHEN
        parsed = AspxClient.parse_aspx_response(raw_data, [
            ParseTarget('maps', as_list=True)
        ])

        # THEN
        expected = {
            'maps': []
        }
        self.assertDictEqual(expected, parsed)

    def test_parse_aspx_data_unofficial_getplayerid(self):
        # GIVEN
        raw_data = 'O\n' \
                   'H\tpid\n' \
                   'D\t81377934\n' \
                   'D\t80842162\n' \
                   '$\t23\t$'
        valid, _ = AspxClient.is_valid_aspx_response(raw_data)
        self.assertTrue(valid)

        # WHEN
        parsed = AspxClient.parse_aspx_response(raw_data, [
            ParseTarget('pids', as_list=True)
        ])

        # THEN
        expected = {
            'pids': [
                {
                    'pid': '81377934'
                },
                {
                    'pid': '80842162'
                }
            ]
        }
        self.assertDictEqual(expected, parsed)

    def test_parse_aspx_data_unofficial_getplayerid_single_result(self):
        # GIVEN
        raw_data = 'O\n' \
                   'H\tpid\n' \
                   'D\t81377934\n' \
                   '$\t14\t$'
        valid, _ = AspxClient.is_valid_aspx_response(raw_data)
        self.assertTrue(valid)

        # WHEN
        parsed = AspxClient.parse_aspx_response(raw_data, [
            ParseTarget('pids', as_list=True)
        ])

        # THEN
        expected = {
            'pids': [
                {
                    'pid': '81377934'
                },
            ]
        }
        self.assertDictEqual(expected, parsed)

    def test_parse_aspx_data_unofficial_getplayerid_no_results(self):
        # GIVEN
        raw_data = 'O\n' \
                   'H\tpid\n' \
                   '$\t5\t$'
        valid, _ = AspxClient.is_valid_aspx_response(raw_data)
        self.assertTrue(valid)

        # WHEN
        parsed = AspxClient.parse_aspx_response(raw_data, [
            ParseTarget('pids', as_list=True)
        ])

        # THEN
        expected = {
            'pids': []
        }
        self.assertDictEqual(expected, parsed)

    def test_parse_aspx_data_error_missing_dataset(self):
        # GIVEN
        raw_data = 'O\n' \
                   'H\tasof\n' \
                   'D\t1663447766\n' \
                   '$\t17\t$'
        valid, _ = AspxClient.is_valid_aspx_response(raw_data)
        self.assertTrue(valid)

        # WHEN/THEN
        self.assertRaises(InvalidResponseError, AspxClient.parse_aspx_response, raw_data, [
            ParseTarget(to_root=True),
            ParseTarget('players', as_list=True)
        ])

    def test_parse_aspx_data_error_missing_parse_target(self):
        # GIVEN
        raw_data = 'O\n' \
                   'H\tasof\n' \
                   'D\t1663447766\n' \
                   'H\tn\tpid\tnick\tscore\n' \
                   'D\t1\t45377286\tmister24\t6458\n' \
                   'D\t2\t500362798\tmister249\t86136\n' \
                   '$\t78\t$'
        valid, _ = AspxClient.is_valid_aspx_response(raw_data)
        self.assertTrue(valid)

        # WHEN/THEN
        self.assertRaises(Error, AspxClient.parse_aspx_response, raw_data, [
            ParseTarget(to_root=True),
        ])
