#! /usr/bin/awk -f
BEGIN {
    # Whether or not we are collecting match data
    match_collect = 0
    match_number = 0

    # There will be a matches array with format:
    ## [[damage_taken, damage, assists, kills, match_id], [info for next match]]
    MATCH_ID = 5
    KILLS = 4
    ASSISTS = 3
    DEATHS = 2
    DAMAGE = 1
    DAMAGE_TAKEN = 0

    while (getline) {
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
    for(i = 0; i <= match_number; i++) {
        print matches[i]
    }
}