
var stype_arr = ["College", "High School", "University"];
// States
var s_a = new Array();
s_a[0]="";
s_a[1]="Conestoga|Centennial|Algonquin|Boréal|Fanshawe|George Brown|Durham|Cambrian|Lambton|Georgian|La Cité|Canadore|Mohawk|Humber|Loyalist|Confederation|Niagara|Michener|St. Lawrence|Northern|Ridgetown|Seneca|Fleming|Sault|St. Clair|Sheridan";
s_a[2]="Central Algoma Secondary School, Desbarats|Chapleau High School, Chapleau|Elliot Lake Secondary School, Elliot Lake|Hornepayne High School, Hornepayne|Korah Collegiate & Vocational School, Sault Ste. Marie|Michipicoten High School, Wawa|Missarenda Secondary School, Missanabie|Prince Charles Secondary School (Sault Ste. Marie), Sault Ste. Marie|Superior Heights Collegiate and Vocational School, Sault Ste. Marie|W. C. Eaket Secondary School, Blind River|White Pines Collegiate & Vocational School, Sault Ste. Marie|École secondaire Carrefour Supérieur-Nord, Wawa|École secondaire l'Orée des Bois, Dubreuilville|Villa Française des Jeunes, Elliott Lake|Holy Angels Learning Centre, Sault Ste. Marie|St. Basil Secondary School, Sault Ste. Marie|St. Mary's College, Sault Ste. Marie|École secondaire catholique Jeunesse-Nord, Blind River|École secondaire Notre-Dame-du-Sault, Sault Ste. Marie|École secondaire Saint-Joseph, Wawa";
s_a[3]="Brock University|Carleton University|College Dominicain|Lakehead University|Laurentian University of Sudbury|McMaster University|Nipissing University|Ontario College of Art|Queen's University|Royal Military College of Canada|Ryerson Polytechnic University|Trent University|University of Guelph|University of Ottawa|University of Toronto|University of Waterloo|Conrad Grebel College|Renison College|St. Jerome's College|St. Paul's United College|University of Western Ontario|University of Windsor|Wilfrid Laurier University|York University|British Columbia Institute of Technology|Open Learning Agency|Royal Roads University|Simon Fraser University|Technical University of British Columbia|Trinity Western University|University of British Columbia|University of Northern British Columbia|University of Victoria";
function populateSchool( stypeElementId, sElementId ) {

	var selectedSIndex = document.getElementById(stypeElementId).selectedIndex;

	var schoolElement = document.getElementById(sElementId);

	schoolElement.length = 0;	// Fixed by Julian Woods
	schoolElement.options[0] = new Option('Select School', '');
	schoolElement.selectedIndex = 0;

	var school_arr = s_a[selectedSIndex].split("|");

	for (var i = 0; i < school_arr.length; i++) {
		schoolElement.options[schoolElement.length] = new Option(school_arr[i], school_arr[i]);
	}
}
function populateStype(stypeElementId, sElementId){
	// given the id of the <select> tag as function argument, it inserts <option> tags
	var stypeElement = document.getElementById(stypeElementId);
	stypeElement.length=0;
	stypeElement.options[0] = new Option('Select School Type','-1');
	stypeElement.selectedIndex = 0;
	for (var i=0; i<stype_arr.length; i++) {
		stypeElement.options[stypeElement.length] = new Option(stype_arr[i],stype_arr[i]);
	}

	// Assigned all countries. Now assign event listener for the states.

	if( sElementId ){
		stypeElement.onchange = function(){
			populateSchool( stypeElementId, sElementId );
		};
	}
}