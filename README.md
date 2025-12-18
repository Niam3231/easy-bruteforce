# Easy Bruteforce
Make bruteforcing passwords much more easy!

Of course, I'm not responible in any way if you do anything with this script and get somehow in trouble.
## Installation
Because its python, it can simply run on anything that runs python. But if you have Linux, the script will allow you to use hashcat after generating.
### Linux
For installing on Linux you need python and the script. This command you can copy-paste and will install everything it requires on Linux including the hashcat feature:
``` bash
sudo apt install -y git python3 hashcat
git clone https://github.com/Niam3231/easy-bruteforce.git && cd easy-bruteforce
echo "In hashes.txt you can place you hashes you want to crack." && echo "Press any key to start the script..." && read
python3 ./generate.py
```
If you don't want to use hashcat you can copy-paste this version, I won't recommend it because you kinda loose the point of it.
``` bash
sudo apt install -y git python3
git clone https://github.com/Niam3231/easy-bruteforce.git && cd easy-bruteforce
echo "In hashes.txt you can place you hashes you want to crack." && echo "Press any key to start the script..." && read
python3 ./generate.py
```
### Windows
On Windows you need to run the python script just as normal. You can find more information how to run python on Windows. Remember that WSL is much better.

[Google Search: How to run python script in Windows](https://www.google.com/search?q=How+to+run+python+script+in+Windows%3F)