window.addEventListener('resize', function() {
    if (getWindowSizeCategory() != last_window_size_category) {
        last_window_size_category = getWindowSizeCategory()
        rebalanceMonthCards()
    }
})