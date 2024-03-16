let parent = document.querySelectorAll(".days");

parent.forEach(function(parent) {
	if (parent.querySelector(".tooltip")) {
		parent.classList.add("fw-bold")
	}
});

document.getElementById("popupBtn").addEventListener("click", function(event) {
	document.getElementById("popup").style.display = "block";
	event.stopPropagation(); 
});

document.getElementById("closeBtn").addEventListener("click", function() {
	document.getElementById("popup").style.display = "none";
});

document.addEventListener("click", function(event) {
	let popup = document.getElementById("popup");
	if (event.target != popup && !popup.contains(event.target)) {
		popup.style.display = "none";
	}
});



function timer()
{
	let today = new Date();

	let hour = today.getHours();
	if (hour<10) hour = "0"+hour;

	let minute = today.getMinutes();
	if (minute<10) minute = "0"+minute;

	let seconds = today.getSeconds();
	if (seconds<10) seconds = "0"+seconds;

	document.getElementById("clock").innerHTML = hour+":"+minute+":"+seconds;
	
	setTimeout("timer()",1000);
};

