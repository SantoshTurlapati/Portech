const express = require('express');
const mysql = require('mysql');
const bodyParser = require('body-parser');
const path = require('path');

const app = express();


app.use(bodyParser.urlencoded({extended:true}));

app.use(express.static('public'));


const db = mysql.createConnection({

host:'localhost',
user:'root',
password:'1234',
database:'portech'

});


db.connect(function(err){

if(err) throw err;

console.log("MySQL Connected");

});


/* REGISTER */

app.post('/registersave',(req,res)=>{

const {fullname,email,username,password} = req.body;

const sql="INSERT INTO users(fullname,email,username,password) VALUES(?,?,?,?)";

db.query(sql,[fullname,email,username,password],(err,result)=>{

if(err) throw err;

res.send("<h2>Registration Successful</h2><a href='login.html'>Login</a>");

});

});


/* LOGIN */

app.post('/login',(req,res)=>{

const username=req.body.username;
const password=req.body.password;

const sql="SELECT * FROM users WHERE username=? AND password=?";

db.query(sql,[username,password],(err,result)=>{

if(result.length>0){

res.sendFile(__dirname+'/public/loginsuccess.html');

}
else{

res.send("Login Failed");

}

});

});


app.listen(3000,function(){

console.log("Server running on http://localhost:3000");

});