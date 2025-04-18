var map = document.querySelector('#map');
var paths = map.querySelectorAll('.map--svg a');
var links = map.querySelectorAll('.map--list a')

//Polyfill du foreach
if(NodeList.prototype.forEach == undefined){
	NodeList.prototype.forEach = function(callback){
		[].forEach.call(this.callback)
	}
}
// active area
var activeArea = function(id){
		map.querySelectorAll('.is-active').forEach(function(item){
			item.classList.remove('is-active');
		})	
		if (id !== undefined) {
			document.querySelector('#list-'+ id).classList.add('is-active')
			document.querySelector('#area-'+id).classList.add('is-active')		
		}

}
// Select item
paths.forEach(function(path){

	path.addEventListener('mouseenter',function(e){
		var id = this.id.replace('area-','')
		activeArea(id)
	})
})

links.forEach(function(link){

	link.addEventListener('mouseenter',function(e){
		var id = this.id.replace('list-','')
		activeArea(id)
	})
})
map.addEventListener('mouseover',function(){
	activeArea();
})









