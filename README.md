
# SeleniumProjects

This repository contain 2 projects.
- LinkedIn 
- GlassDoor

In both projects I have created a script which will act as a bot.


## How It works

- When code is executed bot will created and it will follow below steps

        1. It will open a chrome tab and open LinkedIn or GlassDoor 
        2. It will enter ID and Password (need to add ID and Password info in info.txt file)
        3. After logged in it will open specific url for the given Job title and Job Location 
        4. It will scroll down till the end of page 
        5. It will go to first job post and will click on it 
        6. It will fetch all the information regarding job like job title, company name, Location executed
        7. It will do the same for the next jobs untill the end of page and then it will click on next page and do the same steps again from 4.
        8. It will run till the given number of jobs information you need. 
