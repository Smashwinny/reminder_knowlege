"""Example: private interactive login. Never run with credentials in argv."""
import argparse
import getpass
import json
import os
from pathlib import Path
import sys
import urllib.error
import urllib.parse
import urllib.request


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args):
        return None


def origin(value):
    parsed = urllib.parse.urlsplit(value)
    if (parsed.scheme != 'https' or not parsed.hostname or parsed.username or
            parsed.password or parsed.path not in ('', '/') or parsed.query or parsed.fragment):
        raise ValueError('Use only an HTTPS site origin, with no credentials or path.')
    return value.rstrip('/')


def login(site, username, password):
    request = urllib.request.Request(origin(site) + '/api/auth/login',
        data=json.dumps({'username': username, 'password': password}).encode('utf-8'),
        headers={'Content-Type': 'application/json', 'User-Agent': 'ReminderPrivateLoginExample/1'},
        method='POST')
    opener = urllib.request.build_opener(NoRedirect())
    try:
        with opener.open(request, timeout=45) as response:
            raw = response.read(1024 * 1024 + 1)
            if len(raw) > 1024 * 1024:
                raise ValueError('Login response exceeded the allowed size.')
        result = json.loads(raw)
    except urllib.error.HTTPError as error:
        raise ValueError('Login rejected; HTTP status ' + str(error.code) + '. Response body hidden.') from None
    except (urllib.error.URLError, TimeoutError, UnicodeError, json.JSONDecodeError):
        raise ValueError('Network, certificate or login response error. Details hidden.') from None
    token = result.get('token') if isinstance(result, dict) else None
    user = result.get('user', {}) if isinstance(result, dict) else {}
    if not isinstance(token, str) or not token or '\n' in token or '\r' in token:
        raise ValueError('Login returned no valid session token.')
    return token, user.get('id') if isinstance(user, dict) else None


def save_token(target, token):
    # Exclusive creation preserves any existing session; Unix mode is owner-only.
    fd = os.open(target, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, 'w', encoding='utf-8') as stream:
        stream.write(token + '\n')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--site', default='https://reminder.geniusqi.com')
    parser.add_argument('--root', type=Path, required=True, help='Existing local knowledge/tool workspace')
    parser.add_argument('--save', action='store_true', help='Explicitly create tools/.shiyi_token; refuses overwrite')
    args = parser.parse_args()
    try:
        site = origin(args.site)
        root = args.root.resolve(strict=True)
        tools_dir = root / 'tools'
        if not tools_dir.is_dir() or not tools_dir.resolve().is_relative_to(root):
            raise ValueError('Expected a tools directory inside the workspace.')
        target = tools_dir / '.shiyi_token'
        if args.save and target.exists():
            raise ValueError('Existing token preserved. Use the established credential renewal procedure.')
        if not sys.stdin.isatty():
            raise ValueError('Use a private interactive terminal, not redirected input or a shared log.')
        username = input('Website username: ').strip()
        if not username:
            raise ValueError('Username required.')
        password = getpass.getpass('Website password (hidden): ')
        token, account_id = login(site, username, password)
        if args.save:
            save_token(target, token)
            print('Session saved privately. On Windows, apply the documented file ACL before using the login trigger.')
        else:
            print('Login verified. No session token saved; use --save to create a private session file.')
        if account_id:
            print('Account UUID for PRIVATE server configuration only:', account_id)
        token = password = None
    except ValueError as error:
        print(str(error), file=sys.stderr)
        return 2
    except (OSError, KeyboardInterrupt, EOFError):
        # Avoid displaying request objects, response data or entered secrets.
        print('Login or local save not completed. Existing credentials and task records preserved.', file=sys.stderr)
        return 2
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
