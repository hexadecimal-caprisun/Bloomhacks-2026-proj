const camera = document.getElementById('camera');
const mainContainer = document.querySelector('main');

window.addEventListener("load", getUserCamera());

window.addEventListener('scroll', () => {
    // window.scrollY tells us how many pixels the user has scrolled down
    let scrollDistance = window.scrollY;

    // Multiply the scroll distance by a decimal to make it move slower.
    // 0.5 means it moves at 50% the speed of the foreground.
    // 0.2 means it moves at 20% the speed (very subtle).
    let parallaxSpeed = scrollDistance * 0.5;

    // Apply the new position to the background
    mainContainer.style.backgroundPositionY = `${parallaxSpeed}px`;
});

function getUserCamera(){
    navigator.mediaDevices.getUserMedia({video:true}).then(function(stream){
            camera.srcObject = stream;
        }).catch(function(error){
            console.error(error);
        }
        )
}

