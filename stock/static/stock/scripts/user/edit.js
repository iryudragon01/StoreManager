
var popup= document.getElementById('popup_input')
var verifypwd =document.getElementById('verifypwd')
var veri
function vrfpwd(arg,type){
  if(type==='DELETE'){
  popup.style.top=eval(-50+arg.pageY)+'px'
  popup.style.left=eval(-100+arg.pageX)+'px'
  popup.querySelector('input').value=""
  popup.style.display='block'
  popup.querySelector('input').focus()
  popup.querySelector('input').select()

}else if(type==='submit') {
  verifypwd.value = popup.querySelector('input').value
  document.getElementById('DELETE').click()
}else{
  popup.style.display = 'none'
}

}
