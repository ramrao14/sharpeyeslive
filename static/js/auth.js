var SUPABASE_URL = 'https://zutcwtzondhgzwuygwmj.supabase.co'
var SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inp1dGN3dHpvbmRoZ3p3dXlnd21qIiwicm9sZSI6ImFub24iLCJpYXQiOjE2OTI5OTgwMTgsImV4cCI6MjAwODU3NDAxOH0.MrF7ig3Hy7EA9DpUn7UacKYZS4CpIBnD1MiiuTWmIP0'
var SUPBASE_SERVICE_ROLE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inp1dGN3dHpvbmRoZ3p3dXlnd21qIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTY5Mjk5ODAxOCwiZXhwIjoyMDA4NTc0MDE4fQ.yMmCtkcC9JEaeXwFecKufk5wUHhvrr53v-vt8EkH2Y0'

var supabase = supabase.createClient(SUPABASE_URL, SUPABASE_KEY)

async function signIn() {
  let email = document.getElementById('userEmail').value
  let password = document.getElementById('userPassword').value
  let session = document.getElementById('session')

  const { data, error } = await supabase.auth.signInWithPassword({
    email: email,
    password: password,
  })
  session.value = JSON.stringify(data)
  document.getElementById("loginForm").submit();
}

async function signUp() {
  let email = document.getElementById('userEmailSignup').value
  let password = document.getElementById('userPasswordSignup').value
  let session = document.getElementById('session')

  const { data, error } = await supabase.auth.signUp({
    email: email,
    password: password,
  })
  console.log(data)
  console.log(error)
  session.value = JSON.stringify(data)
  document.getElementById("signupForm").submit()
}

async function signOut() {
  const { error } = await supabase.auth.signOut()
  window.location.replace("/auth");
}

function displaySignup(){
  document.getElementById('loginSection').setAttribute('style', 'display: none')
  document.getElementById('signupSection').setAttribute('style', 'display: block')
}

function displayLogin(){
  document.getElementById('signupSection').setAttribute('style', 'display: none')
  document.getElementById('loginSection').setAttribute('style', 'display: block')
}


async function getInviteLink() {
  const { data, error } = await supabase.auth.admin.inviteUserByEmail('ramg99@yahoo.com')
  console.log(data)
  console.log(error)
}
