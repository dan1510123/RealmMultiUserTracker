#! /usr/bin/awk -f
BEGIN {
    #Print header and in-line css and js to begin html file
    print "Content-type: text/html\n"
    print "<html>\n\
    <head>\n\
        <style>\n\
                html{
                height: 100%;
                }

                body {
                height:100%;
                background-color: #1e1c2e;
                background-color: #151320;
                background-color: #0f0e16;
                color: #cccccc;
                }

                #title{
                padding: 20px;
                font-size: 40px;
                border-radius: 15px 15px 0 0;
                background-image: linear-gradient(-30deg, #1b1b1b 50%, #23235c);
                }

                .fullContainer{
                font-family: Arial;
                font-size: 30px;
                margin: 50px 100px;
                background-color: #1b1b1b;
                border-radius: 15px;
                box-sizing: border-box;
                box-shadow: -7px 7px 10px rgb(0,0,0,0.8);
                }

                .resultsContainer{
                width: 100%;
                display: flex;
                flex-direction: row;
                flex-wrap: nowrap;
                }

                .playerOutput{
                flex: 1;
                flex-basis: 1;
                padding: 0 15px 15px 15px;
                }

                .matchesTable {
                font-size: 20px;
                border-collapse: collapse;
                width: 100%;
                border: 1px solid #363636;
                }

                .playerName{
                padding: 25px 8px;
                font-weight: bold;
                }

                th, td {
                text-align: left;
                padding: 8px;
                }
                th{
                font-weight: normal;
                background-color: #2f2f6a;
                font-size: 14px;
                }

                tr:nth-child(even){
                background-color: #262626;
                }


                tr:first-child{
                border: 1px solid #363636;
                }

                tr{
                cursor: pointer;
                transition: .2s;
                }

                .noPointer{
                cursor: default;
                
                }
                tr:hover {background-color: #242442;}


        </style>\n\
        <script>\n\
            document.addEventListener(\"DOMContentLoaded\", () => {\n\
                const rows = document.querySelectorAll(\"tr[data-href]\");\n\
                rows.forEach(row =>{\n\
                    row.addEventListener(\"click\", () => {\n\
                    window.location.href = row.dataset.href;\n\
                    });\n\
                });\n\
            });\n\
        </script>\n\
    </head>\n\
    <body>\n\
        <div class=\"fullContainer\">\n\
            <div id=\"title\">Realm Multi-User Tracker</div>\n\
                <div class=\"resultsContainer\">\n"

    

    #get usernames
    playercount = 0
    split(ENVIRON["QUERY_STRING"],people,"&")
    for (i in people) { split(people[i],names,/=/); cgidat[names[1]] = names[2] }
    for(n in cgidat){
        if(cgidat[n] != "") {
            # print cgidat[n]
            sub(cgidat[n], "+", "-")
            playercount++
        }
    }
    # print playercount

    # There will be a matches array with format:
    ## [[damage_taken, damage, assists, kills, match_id], [info for next match]]
    MATCH_ID = 6
    KILLS = 5
    ASSISTS = 4
    DEATHS = 3
    PLACEMENT = 2
    DAMAGE = 1

    #getData for each person
    for (i = 0; i < playercount; i++){
        # print cgidat[i]
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
            else if(match($0, /placement/) && match_collect == 1 && match_index == 4) {
                gsub(/ /, "")
                gsub(/\n/, "")
                gsub(/"placement":/, "")
                gsub(/,/, "")
                matches[match_number] = "" + $0 "," matches[match_number]
                match_index++
            }
            else if(match($0, /damage/) && match_collect == 1 && match_index == 5) {
                gsub(/ /, "")
                gsub(/\n/, "")
                gsub(/"damage":/, "")
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
        
        # Start the player's table and add their username
        print "                    <div class=\"playerOutput\">\n\
                        <div class=\"playerName\">\n\
                            " cgidat[i] "\n\
                        </div>\n\
                        <table class=\"matchesTable\">\n\
                            <tr class=\"noPointer\">\n\
                                <th>Place</th>\n\
                                <th>DMG</th>\n\
                                <th>K</th>\n\
                                <th>A</th>\n\
                            </tr>\n"

        # Go through each match of the player
        for(m = 0; m < match_number; m++) {
            split(matches[m], match_stats, ",")
            # Get match link
            print "                            <tr data-href=\"https://realmtracker.com/match/pc/" ""+match_stats[MATCH_ID] "\">\n"
            # Get Place, Damage, Kills, and Assists
            print "                                <td>" match_stats[PLACEMENT] "</td>\n"
            print "                                <td>" match_stats[DAMAGE] "</td>\n"
            print "                                <td>" match_stats[KILLS] "</td>\n"
            print "                                <td>" match_stats[ASSISTS] "</td>\n"
            print "                            </tr>\n"
        }

        # End the table
        print "                        </table>\n\
                    </div>\n"
    }

    print "                </div>\n\
            </div>\n\
        </div>\n\
    </body>\n\
</html>"

}