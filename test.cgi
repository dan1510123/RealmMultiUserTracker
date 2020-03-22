#! /usr/bin/awk -f
BEGIN {
    print "Content-type: text/html\n"
    print "Hello world."
    print"<pre>"

    #get usernames
    playercount = 0
    split(ENVIRON["QUERY_STRING"],people,"&")
    for (i in people) { split(people[i],names,/=/); cgidat[names[1]] = names[2] }
    for(n in cgidat){
        if(n != "") {
            print cgidat[n]
            playercount++
        }
    }

    #getData for each person
    
    for (i = 0; i < personCount; ++i){
        rawData = system("wget -qO- https://apex.tracker.gg/profile/pc/" names[i])
        cleanData = system("awk -f scrape_user.awk" rawData)
        allData[i] = cleanData
    }

    print allData[0]
    print allData[1]

}


