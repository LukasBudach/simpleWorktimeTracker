function rebalanceMonthCards() {
    let card_group = document.getElementById('month-cards')
    let cards = resortCards(card_group.children)
    

    if (last_window_size_category == -1) {
        last_window_size_category = getWindowSizeCategory()
    }
    
    if (last_window_size_category == 0) {
        // smallest, do nothing, sorted is perfect in this case
    } else if (last_window_size_category == 1) {
        // two cards per row, rebalance
        cards = calcRebalanceTwoCols(cards)
    } else {
        // three cards per row, rebalance
        cards = calcRebalanceThreeCols(cards)
    }
    
    cards.forEach(card => {
        card_group.removeChild(card)
        card_group.appendChild(card)
    })
}

function calcRebalanceTwoCols(sorted_cards) {
    let n = sorted_cards.length
    
    let cards = sorted_cards
    
    if (Math.floor(n/2) != 0) {
        let columns = [[],[]]
        let col_ctr = 0
        
        cards.forEach(card => {
            columns[col_ctr].push(card)
            col_ctr = (col_ctr + 1) % 2
        })
        
        cards = columns[0].concat(columns[1])
    }
    
    return cards
}

function calcRebalanceThreeCols(sorted_cards) {
    let n = sorted_cards.length
    
    let cards = sorted_cards
    
    if (Math.floor((n - 1) / 3) != 0) {
        let columns = [[],[],[]]
        let col_ctr = 0
        
        if ((n % 3) == 1) {
            let rows_filled = Math.floor(n/3) - 1
            let inserted_ctr = 0
            
            cards.forEach(card => {
                columns[col_ctr].push(card)
                if (Math.floor(inserted_ctr / 3) < rows_filled) {
                    col_ctr = (col_ctr + 1) % 3
                    inserted_ctr += 1
                } else {
                    col_ctr = (col_ctr + 1) % 2
                }
            })            
        } else {
            cards.forEach(card => {
                columns[col_ctr].push(card)
                col_ctr = (col_ctr + 1) % 3
            })
        }
        
        cards = columns[0].concat(columns[1].concat(columns[2]))
    }
    
    return cards
}

function resortCards(cards) {
    let sorted_cards = Array(cards.length)
    
    for (let card of cards) {
        sorted_cards[card.id.split('-')[1]] = card
    }
    
    return sorted_cards
}
