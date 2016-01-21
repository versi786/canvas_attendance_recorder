import sys
import requests
import json

class colors:
    GREEN = '\x1B[32m'
    RED = '\x1B[31m'
    ENDC = '\033[0m'

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
        readline = readline.split('^');
        name = readline[1]
        pennid = readline[0][8:-2]
        pay = 'grade_data[sis_user_id:' + pennid.strip()
        pay += '][posted_grade]'
        payload = {pay:1} #grade is set to 1 for completion
        headers = {'Authorization': 'Bearer ' + authkey}
        #initial reqeust to post grade
        r = requests.post(url=link, data=payload, headers=headers)
        r = json.loads(r.text)

        #get the status url
        r = requests.get(r['url'])
        r = json.loads(r.text);

        #keep checking until ist is no longer running
        while (r['workflow_state'] == 'running'):
            r = requests.get(r['url'])
            r = json.loads(r.text);

        #give meaningful message to student
        if(r['workflow_state'] == 'completed'):
            print (colors.GREEN + 'Attendance successfully recorded for: ' +
                name + colors.ENDC)
        else:
            print (colors.RED + 'Error recording attendance for: ' + name +
            colors. ENDC)


if __name__ == "__main__":
    main()
