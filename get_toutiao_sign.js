i = {url:process.argv[2]};
a = require('./toutiao_sign.js');
n = a.sign;
console.log(n.call(a,i));