#! /usr/bin/awk -f
BEGIN {
    print "Content-type: text/html\n"
    print "<html>\n  <head>"

    #get usernames
    playercount = 0
    split(ENVIRON["QUERY_STRING"],people,"&")
    for (i in people) { split(people[i],names,/=/); cgidat[names[1]] = names[2] }
    for(n in cgidat){
        if(cgidat[n] != "") {
            print cgidat[n]
            playercount++
        }
    }
    print playercount

    # There will be a matches array with format:
    ## [[damage_taken, damage, assists, kills, match_id], [info for next match]]
    MATCH_ID = 5
    KILLS = 4
    ASSISTS = 3
    DEATHS = 2
    DAMAGE = 1
    DAMAGE_TAKEN = 0

    #getData for each person
    for (i = 0; i < playercount; i++){
        print cgidat[i]
        rawData = "wget -qO- https://realmtracker.com/profile/pc/"cgidat[i]
        
        # Whether or not we are collecting match data
        match_collect = 0
        match_number = 0
        
        
        while ((rawData | getline) > 0) {
            if(match($0, /<script.*var imp_matchHistory = \[.*/)) {
                match_collect = 1
            }
            else if(match($0, /match_id/) && match_collect == 1 && match_index == 0) {
                gsub(/ /, "")
                gsub(/\n/, "")
                gsub(/"match_id":/, "")
                gsub(/,/, "")
                matches[match_number] = $0
                match_index++
            }
            else if(match($0, /kills/) && match_collect == 1 && match_index == 1) {
                gsub(/ /, "")
                gsub(/\n/, "")
                gsub(/"kills":/, "")
                gsub(/,/, "")
                matches[match_number] = "" + $0 "," matches[match_number]
                match_index++
            }
            else if(match($0, /assists/) && match_collect == 1 && match_index == 2) {
                gsub(/ /, "")
                gsub(/\n/, "")
                gsub(/"assists":/, "")
                gsub(/,/, "")
                matches[match_number] = "" + $0 "," matches[match_number]
                match_index++
            }
            else if(match($0, /deaths/) && match_collect == 1 && match_index == 3) {
                gsub(/ /, "")
                gsub(/\n/, "")
                gsub(/"deaths":/, "")
                gsub(/,/, "")
                matches[match_number] = "" + $0 "," matches[match_number]
                match_index++
            }
            else if(match($0, /damage/) && match_collect == 1 && match_index == 4) {
                gsub(/ /, "")
                gsub(/\n/, "")
                gsub(/"damage":/, "")
                gsub(/,/, "")
                matches[match_number] = "" + $0 "," matches[match_number]
                match_index++
            }
            else if(match($0, /damage_taken/) && match_collect == 1 && match_index == 5) {
                gsub(/ /, "")
                gsub(/\n/, "")
                gsub(/"damage_taken":/, "")
                gsub(/,/, "")
                matches[match_number] = "" + $0 "," matches[match_number]
                match_index = 0
                match_number++
            }
            if(match_number == 10) {
                match_collect = 0
            }
        }
        close(rawData)
        
        for(m = 0; m < match_number; m++) {
            print matches[m]
            print "Match"
        }
        print "Player"
    }

    print "  </head>\n</html>"
}