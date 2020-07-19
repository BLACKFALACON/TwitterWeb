/* ---------------------- PAROLA GÖSTER  -------------------------- */
function passwordG() {
  var passwordInput = document.getElementById('id_password');
  var passStatus = document.getElementById('iconDurum');
  if (passwordInput.type == 'password'){
    passwordInput.type='text';
    passStatus.className='fa fa-eye-slash';
    
  }
  else{
    passwordInput.type='password';
    passStatus.className='fa fa-eye';
  }
}
/* ---------------------- PAROLA GÖSTER SON   -----------------------*/

/* -------------------------- AÇILIR KAPANIR MENÜ -------------- */

var coll = document.getElementsByClassName("collapsible");
var i;
var time=new Date().getHours();
var durum;
for (i = 0; i < coll.length; i++) 
{
  coll[i].addEventListener("click", function() 
  {
    this.classList.toggle("active");
    var content = this.nextElementSibling;
    if (content.style.maxHeight)
    {
      content.style.maxHeight = null;
    } 
    else 
    {
      content.style.maxHeight = content.scrollHeight + "px";
    } 
  });
}
/* -------------------------- AÇILIR KAPANIR MENÜ SON --------------  */

/* --------------------- KAYAN YAZI ------------------------- */

var i = 0;
var txt = ' Twitter Analiz';
var speed = 50;
function typeWriter() {
  if (i < txt.length) {
    document.getElementById("baslık").innerHTML += txt.charAt(i);
    i++;
    setTimeout(typeWriter, speed);
  }
}

function Gizle()
{
  document.getElementById("Gizle").style.display="none";
}
function openCity(evt, cityName) 
{
  var i, main, tablinks;
  main = document.getElementsByClassName("main");

  for (i = 0; i < main.length; i++) {
    main[i].style.display = "none";  
  }
  tablinks = document.getElementsByClassName("tablinks");
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" active", "");
  }
  document.getElementById(cityName).style.display = "block";
  evt.currentTarget.className += " active";
}

/* --------------------- KAYAN YAZI SON ---------------------------------- */


/* -----------------------  MODAL SON -------------- */
function modalac()
{
  document.getElementById('cikis').style.display='block';
}
function modalkapat()
{
  document.getElementById('cikis').style.display='none';
}

var cikismodal = document.getElementById('cikis');
window.onclick = function(event)
{
  if (event.target == cikismodal) 
  {
   cikismodal.style.display = "none";
  }
}
/* ----------------------- MODAL SON-------------- */
