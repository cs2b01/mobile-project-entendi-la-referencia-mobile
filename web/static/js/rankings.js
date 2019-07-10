$.getJSON("/current", function(data){
         if(data==null){
          window.location.href="http://3.130.238.73/dologin"
         }
             });

function Aportes() {
     var url = "http://3.130.238.73/rankings_uploads";
    $("#grid").dxDataGrid({
        dataSource: DevExpress.data.AspNet.createStore({
            key: "id",
            loadUrl: url,
            onBeforeSend: function(method, ajaxOptions) {
                ajaxOptions.xhrFields = { withCredentials: true };
            }
        }),
        remoteOperations: true,
        columns: [
            {dataField: "username"},
            {dataField: "name"},
            {dataField: "lastname"},
            {dataField: "uploads"}
        ],
        height: 350,
        width:600,
        editing: {
            allowAdding: false,
            allowUpdating: false,
            allowDeleting: false
        },
        grouping: {
            autoExpandAll: false
        }

    }).dxDataGrid("instance");

}

function Correctas(){
     var url = "http://3.130.238.73/rankings_record";
    $("#grid").dxDataGrid({
        dataSource: DevExpress.data.AspNet.createStore({
            key: "id",
            loadUrl: url,
            onBeforeSend: function(method, ajaxOptions) {
                ajaxOptions.xhrFields = { withCredentials: true };
            }
        }),
        remoteOperations: true,
        columns: [
            {dataField: "username"},
            {dataField: "name"},
            {dataField: "lastname"},
            {dataField: "record"}
        ],
        height: 350,
        width:600,
        editing: {
            allowAdding: false,
            allowUpdating: false,
            allowDeleting: false
        },
        grouping: {
            autoExpandAll: false
        }

    }).dxDataGrid("instance");
}


