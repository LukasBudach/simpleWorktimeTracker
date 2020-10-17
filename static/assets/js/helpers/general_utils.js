function getWindowSizeCategory() {
    let width = window.innerWidth
    
    if (width < 680) {
        return 0
    } else if (width < 1020) {
        return 1
    }
    return 2
}