var domain='http://localhost:8000/'

window.onload = function() {
	var list = document.getElementById('list');

	var ruricListLoader = new XMLHttpRequest()
	ruricListLoader.onreadystatechange = function(){
		if (ruricListLoader.readyState == 4) {
			if (ruricListLoader.status == 200){
				var data = JSON.parse(ruricListLoader.responseText);
				var s = '<ul>';
				for (i = 0; i < data.lenght; i++) {
					s += '<li>' + data[i].name + '</li>';
				}
				s += '</ul>'
				list.innerHTML = s;
			}
		}
	}
	function rubricListLoad(){
		ruricListLoader.open('GET', domain + 'api/rubrics/', true);
		ruricListLoader.send();
	}
	rubricListLoad();
}