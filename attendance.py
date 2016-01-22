import sys
import requests
import json

class colors:
    GREEN = '\x1B[32m'
    RED = '\x1B[31m'
    ENDC = '\033[0m'

CURSOR_UP_ONE = '\x1b[1A'
ERASE_LINE = '\x1b[2K'

classID = str(1299906)
authKey = 'token.txt'

def main():

    if(len(sys.argv) != 2):
        print("Usage: python attendance.py <assignment id>")
        sys.exit(1)

    # create post url
    link = sys.argv[1];
    link = 'https://canvas.upenn.edu/api/v1/courses/' + classID + '/assignments/' + link
    link += '/submissions/update_grades'

    # get the api key
    f = open(authKey, 'r')
    authkey = f.read().strip()

    while(True):
        #parse penn key and create request
        readline = sys.stdin.readline()

        if(readline.startswith('exit')):
            sys.exit(0)
        #remove personal information from screen so next student can not read
        print (CURSOR_UP_ONE + ERASE_LINE + CURSOR_UP_ONE)
        print 'Processing...'
        try:
            readline = readline.split('^');
            name = readline[1]
            pennid = readline[0][8:-2]
            pay = 'grade_data[sis_user_id:' + pennid.strip()
            pay += '][posted_grade]'
        except:
            print 'error parsing ID Card'
            continue
        payload = {pay:1} #grade is set to 1 for completion
        headers = {'Authorization': 'Bearer ' + authkey}
        #initial reqeust to post grade
        r = requests.post(url=link, data=payload, headers=headers)

        #get the status url
        r = json.loads(r.text)
        r = requests.get(r['url'])

        #keep checking until ist is no longer running
        r = json.loads(r.text);
        while (r['workflow_state'] == 'running'):
            r = requests.get(r['url'])
            r = json.loads(r.text);

        print (CURSOR_UP_ONE + ERASE_LINE + CURSOR_UP_ONE)
        #give meaningful message to student
        if(r['workflow_state'] == 'completed'):
            print (colors.GREEN + 'Attendance successfully recorded for: ' +
                name + colors.ENDC)
        else:
            print (colors.RED + 'Error recording attendance for: ' + name +
            colors. ENDC)


if __name__ == "__main__":
    main()
