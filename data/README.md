## For COMPSCIWinter26: 
- obtained from this link: https://client.scalar.com/workspace/default/request/ozjSXCjy4oINmUeEM7XpK
- obtained from query: /v2/rest/websoc?department=COMPSCI&year=2026&quarter=Winter
- all COMPSCI courses offered during winter quarter 2026
- removed all courses whose number starts with a 2
- removed all courses specific to honors whose number starts with an H

## For CSUpperDivFullResponse:
- obtained from this query:
![alt text](image.png)
- ran this command in terminal to condense the "terms" array formatting: python "c:\Users\alyta\Desktop\Classes\CS 125\cs125\scripts\reformat_arrays.py" "c:\Users\alyta\Desktop\Classes\CS 125\cs125\data\COMPSCIUpperDiv.json" "c:\Users\alyta\Desktop\Classes\CS 125\cs125\data\COMPSCIUpperDiv.reformatted.json"
- removed all courses whose title matches COMPSCI2**, mostly from the dependencies array

## For CSUpperDivStripped:
- took all elements in CSUpperDivFullResponse and ran it through the strip_courses.py script
- only kept relevant fields needed for our mongodb table

## Please place information for each .json in this /data folder here.