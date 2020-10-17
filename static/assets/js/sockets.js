socket.on('connect', () => {
    socket.emit('connected')
})

socket.on('createCard', (month, year, required_time, time_done) => {
    console.log('Creating Card...')
    addMonthCard(month, year, required_time, time_done)
})

socket.on('updateHeader', (total_time, required_time, total_overtime, is_overtime_negative) => {
    set_total_time_done(total_time.split(':')[0], total_time.split(':')[1])
    set_total_time_required(required_time.split(':')[0], required_time.split(':')[1])
    set_total_overtime(is_overtime_negative ? total_overtime.split(':')[0].slice(1) : total_overtime.split(':')[0],
                       total_overtime.split(':')[1], is_overtime_negative)
})

socket.on('updateYearDropdown', years => {
    populate_year_selection(years)
})