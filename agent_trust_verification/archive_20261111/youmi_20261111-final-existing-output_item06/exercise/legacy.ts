type Legacy = {approved:boolean; sent:boolean};
const impossible:Legacy={approved:false,sent:true};
console.log(JSON.stringify(impossible));
