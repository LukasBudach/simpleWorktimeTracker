function set_total_time_done(hours, minutes) {
    let content = document.getElementById('total-time-done')
    content.innerText = hours + ' h ' + ('0' + minutes).slice(-2) + ' min'
}

function set_total_time_required(hours, minutes) {
    let content = document.getElementById('total-time-required')
    content.innerText = hours + ' h ' + ('0' + minutes).slice(-2) + ' min'
}

function set_total_overtime(hours, minutes, is_negative) {
    let content = document.getElementById('total-overtime')
    content.innerText = (is_negative ? '- ' : '') + hours + ' h ' + ('0' + minutes).slice(-2) + ' min'
}