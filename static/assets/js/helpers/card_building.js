function getMonthCard(month, year, required_time, time_done) {
    let card = document.createElement('DIV')
    card.className = 'card'
    
    card.appendChild(getMonthCardTitle(month + ' ' + year))
    card.appendChild(getMonthCardBody(required_time, time_done))
    
    return card
}

function getMonthCardTitle(text) {
    let header = document.createElement('DIV')
    header.className = 'card-header'
    
    let header_title = document.createElement('H5')
    header_title.className = 'mb-0'
    header_title.innerText = text
    
    header.appendChild(header_title)
    return header
}

function getMonthCardBody(required_time, time_done) {
    let body = document.createElement('DIV')
    body.className = 'card-body'
    body.appendChild(getMonthCardBodyTable(required_time, time_done))
    
    return body
}

function getMonthCardBodyTable(required_time, time_done) {
    let table_wrapper = document.createElement('DIV')
    table_wrapper.className = 'table-responsive table-borderless'
    
    let table = document.createElement('TABLE')
    table.className = 'table table-bordered'
    
    let table_body = document.createElement('TBODY')
    table_body.appendChild(getMonthCardBodyTableRequiredRow(required_time))
    table_body.appendChild(getMonthCardBodyTableDoneRow(time_done))
    
    table.appendChild(table_body)
    
    table_wrapper.appendChild(table)
    
    return table_wrapper
}

function getMonthCardBodyTableRequiredRow(required_time) {
    return getMonthCardBodyTableRow('Time Required', required_time)
}
    
function getMonthCardBodyTableDoneRow(time_done) {
    return getMonthCardBodyTableRow('Time Done', time_done)
}

function getMonthCardBodyTableRow(descriptor, value) {
    let row = document.createElement('TR')
    
    let desc = document.createElement('TD')
    desc.className = 'td-field-descriptor'
    desc.innerText = descriptor
    
    let val = document.createElement('TD')
    val.innerText = value
    
    row.appendChild(desc)
    row.appendChild(val)
    
    return row
}