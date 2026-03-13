function scrollCars(direction) {
    const slider = document.getElementById("carSlider");
    const scrollAmount = 700;
    slider.scrollLeft += direction * scrollAmount;
}