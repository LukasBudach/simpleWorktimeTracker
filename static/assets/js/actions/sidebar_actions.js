function populate_year_selection(years) {
    let year_selection_menu = document.getElementById('year-select-menu')
    let child_count = year_selection_menu.childElementCount
    
    for (let i = 0; i < child_count; i++) {
        year_selection_menu.removeChild(year_selection_menu.children[0])
    }

    let menu_item = document.createElement('A')
    menu_item.className = 'dropdown-item'
    menu_item.href = '?year=all'
    menu_item.innerText = 'All Years'
    
    year_selection_menu.appendChild(menu_item)
    
    years.forEach(year => {
        menu_item = document.createElement('A')
        menu_item.className = 'dropdown-item'
        menu_item.href = '?year=' + year
        menu_item.innerText = year
        
        year_selection_menu.appendChild(menu_item)
    })
}