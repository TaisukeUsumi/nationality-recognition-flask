function previewImage(event)
{
	var fileReader = new FileReader();
	fileReader.onload = (function() {
		document.getElementById('input_image').src = fileReader.result;
	});
	fileReader.readAsDataURL(event.files[0]);
}

document.getElementById('form').onsubmit = function() {
	document.getElementById('input_message').textContent = "Predicting";
	document.getElementById('input_image').src = "static/loading.gif"; 
	document.getElementById('form').style.visibility = "hidden";
}