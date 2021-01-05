from subprocess import PIPE, Popen
import time


def str_time_now():
    n = time.gmtime()
    return str(n[3]) + ':' + str(n[4]) + ':' + str(n[5])


def cmdline(command):
    process = Popen(args=command, stdout=PIPE, shell=True)
    return process.communicate()[0]


def check_program_is_installed(program, args, affected_tools):
        try:
            Popen([program, args], stderr=PIPE, stdout=PIPE)
            return True
        except EnvironmentError:
            # handle file not found error.
            # the config file is installed in:
            msg = "\n** {0} not found. This program is needed for the following " \
                  "tools to work properly:\n   {1}\n   {0} " \
                  " \n".format(program, affected_tools)
            print(msg)

        except Exception as e:
            print("Error: {}".format(e))
        return False


def is_apache_installed() -> bool:
    return check_program_is_installed('apache2', 'status', 'webserver')


def is_php_installed() -> bool:
    return check_program_is_installed('php', '-v', 'webserver')


def is_mysql_installed() -> bool:
    return check_program_is_installed('mysql', '-V', 'webserver')


def is_proftp_installed() -> bool:
    return check_program_is_installed('proftp', '--version', 'webserver')


def is_clamav_installed() -> bool:
    return check_program_is_installed('clamdscan', '-V', 'security')
