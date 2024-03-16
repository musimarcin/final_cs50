let parent = document.querySelectorAll(".days");

parent.forEach(function(parent) {
	if (parent.querySelector(".tooltip")) {
		parent.classList.add("fw-bold")
	}
});

let popupbtn = document.querySelectorAll(".popupBtn");
let popup = document.querySelector(".popup");
let closebtn = document.querySelectorAll(".closeBtn");

popupbtn.forEach(e => 
	{
	e.addEventListener("click", function(event) 
		{
			popup.style.display = "block";
			event.stopPropagation(); 
		})
	});

closebtn.forEach(e => 
	{
	e.addEventListener("click", function() 
		{
			popup.style.display = "none";
		});
	})

document.addEventListener("click", function(event) {
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

