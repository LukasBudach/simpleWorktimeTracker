function addMonthCard(month, year, required_time, time_done) {
    let card_group = document.getElementById('month-cards')
    
    let card = getMonthCard(month, year, required_time, time_done)
    card.id = "mcard-" + card_group.children.length
    
    card_group.appendChild(card)
    
    rebalanceMonthCards()
}