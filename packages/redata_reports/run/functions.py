from datetime import datetime
from os import environ
import requests
import simplejson as json

report_date = None


def get_request_headers():
    """
    Returns the headers to use for the figshare requests.get calls
    """
    headers = {'Content-Type': 'application/json',
               'Authorization': 'Bearer {0}'.format(environ['API_TOKEN'])}
    return headers


def get_report_date():
    """
    Returns a timestamp that is the date and time of data retrieval
    """
    global report_date
    if not report_date:
        report_date = datetime.now()
    return report_date


def sync_to_dashboard(data, report):
    """
    Sends the given data to the Google Sheet given by report via the sheet's POST request url
    """
    print(f'Sending data for report "{report}" to dashboard')

    if not data:
        return 'No data to send'

    postdata = {"action": "insertupdate",
                "sheet": report,
                "accesskey": environ['GSHEETS_DASHBOARD_KEY'],
                "data": data}

    with open('data.json', 'w') as jsonfile:
        json.dump(postdata, jsonfile)

    response = requests.post(environ['GSHEETS_DASHBOARD_POST_URL'],
                             headers={'Content-Type': 'application/json'},
                             json=postdata)

    result = ''
    if response.status_code == 200:
        result = response.content
    else:
        result = f'Request to dashboard sheet returned code {response.status_code}'

    return result


def format_bytes(bytes, unit, append_unit=False, SI=False):
    # https://stackoverflow.com/a/52684562
    """
    Converts bytes to common units such as kb, kib, KB, mb, mib, MB

    Parameters
    ---------
    bytes: int
        Number of bytes to be converted

    unit: str
        Desired unit of measure for output


    SI: bool
        True -> Use SI standard e.g. KB = 1000 bytes
        False -> Use JEDEC standard e.g. KB = 1024 bytes

    Returns
    -------
    str:
        E.g. "7 MiB" where MiB is the original unit abbreviation supplied
    """
    if unit == "B" or unit.lower() in "byte bytes":
        return bytes
    if unit.lower() in "b bit bits".split():
        return f"{bytes * 8}" + f' {unit}' if append_unit else ''
    unitN = unit[0].upper() + unit[1:].replace("s", "")  # Normalised
    reference = {"Kb Kib Kibibit Kilobit": (7, 1),
                 "KB KiB Kibibyte Kilobyte": (10, 1),
                 "Mb Mib Mebibit Megabit": (17, 2),
                 "MB MiB Mebibyte Megabyte": (20, 2),
                 "Gb Gib Gibibit Gigabit": (27, 3),
                 "GB GiB Gibibyte Gigabyte": (30, 3),
                 "Tb Tib Tebibit Terabit": (37, 4),
                 "TB TiB Tebibyte Terabyte": (40, 4),
                 "Pb Pib Pebibit Petabit": (47, 5),
                 "PB PiB Pebibyte Petabyte": (50, 5),
                 "Eb Eib Exbibit Exabit": (57, 6),
                 "EB EiB Exbibyte Exabyte": (60, 6),
                 "Zb Zib Zebibit Zettabit": (67, 7),
                 "ZB ZiB Zebibyte Zettabyte": (70, 7),
                 "Yb Yib Yobibit Yottabit": (77, 8),
                 "YB YiB Yobibyte Yottabyte": (80, 8),
                 }
    key_list = '\n'.join(["     b Bit"] + [x for x in reference.keys()]) + "\n"
    if unitN not in key_list:
        raise IndexError(f"\n\nConversion unit must be one of:\n\n{key_list}")
    units, divisors = [(k, v) for k, v in reference.items() if unitN in k][0]
    if SI:
        divisor = 1000**divisors[1] / 8 if "bit" in units else 1000**divisors[1]
    else:
        divisor = float(1 << divisors[0])
    value = bytes / divisor
    # return f"{value:,.0f} {unitN}{(value != 1 and len(unitN) > 3)*'s'}"
    return f"{value:.2f}" + f' {unit}' if append_unit else f"{value:.2f}"


def get_report_outfile(reportname, prefix=''):
    """
    Returns a writable file in the current directory

    reportname: str
        The name of the file to use. If it starts with '$$*$$', then prefix will be used

    prefix: str
        This string will be prefixed to a time stamep to form the file name
    """
    filename = reportname
    if reportname.startswith('$$*$$'):
        filename = reportname.replace('$$*$$', prefix)
    return open(filename, "w", encoding='utf-8')
