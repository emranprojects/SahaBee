# SahaBee's Soldier
An agent that automatically downloads and emails the timesheet excel.  
## Install prereqs
```bash
cat soldier/requirements-apt.txt | xargs sudo apt-get install
```
## Usage
```bash
./soldier/send-timesheet.sh --server <SMTP_SERVER:PORT> --user <USER> --pass <PASS> --to <RECIPIENT> --year-month <LIKE 1400/01> --sahabee-user <user of sahabee.ir>
```
