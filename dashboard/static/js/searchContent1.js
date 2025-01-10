const tableOutput=document.querySelector(".table-output");
const appTable=document.querySelector(".app-table");
const paginationContainer=document.querySelector(".pagination-container");
const tbody=document.querySelector('.table-body')
tableOutput.style.display="none";
function searchfn(e){
    const searchValue=e.target.value;
    if(searchValue.trim().length>0){
        paginationContainer.style.display="none";
        tbody.innerHTML="";
        fetch('/search-content1',{
            body:JSON.stringify({searchText:searchValue}),
            method:"POST",
        }).then(response=>response.json()).then(
            data=>{
                console.log("Search data",data);
                tableOutput.style.display='block';
                appTable.style.display='none';
                if(data.length===0){
                    tableOutput.innerHTML='No results found';
                }else{
                   data.forEach(item=>{
                    tbody.innerHTML+=`
                    <tr>
                        <td>${item.amount}</td>
                        <td>${item.source}</td>
                        <td>${item.description}</td>
                        <td>${item.date}</td>
                    </tr>`;
                   })
                }
            }
        );
    }else{
        appTable.style.display='block';
        paginationContainer.style.display="block";
        tableOutput.style.display='none';
    }
}