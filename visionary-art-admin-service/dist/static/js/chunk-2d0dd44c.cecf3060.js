(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-2d0dd44c"],{8152:function(t,e,n){"use strict";n.r(e);var l=function(){var t=this,e=t.$createElement,n=t._self._c||e;return n("div",{staticClass:"app-container"},[n("el-table",{directives:[{name:"loading",rawName:"v-loading",value:t.listLoading,expression:"listLoading"}],attrs:{data:t.list,"element-loading-text":"Loading",border:"",fit:"","highlight-current-row":""}},[n("el-table-column",{attrs:{label:"ID",align:"center",width:"95"},scopedSlots:t._u([{key:"default",fn:function(e){return[t._v(" "+t._s(e.row.id)+" ")]}}])}),n("el-table-column",{attrs:{label:"Sender UID",align:"center"},scopedSlots:t._u([{key:"default",fn:function(e){return[t._v(" "+t._s(e.row.uid)+" ")]}}])}),n("el-table-column",{attrs:{label:"Title",align:"center"},scopedSlots:t._u([{key:"default",fn:function(e){return[n("span",[t._v(t._s(e.row.title))])]}}])}),n("el-table-column",{attrs:{"class-name":"status-col",label:"Tag",align:"center"},scopedSlots:t._u([{key:"default",fn:function(e){return[n("el-tag",{attrs:{type:t._f("statusFilter")(e.row.tag)}},[t._v(t._s(e.row.tag))])]}}])}),n("el-table-column",{attrs:{label:"Contact",align:"center"},scopedSlots:t._u([{key:"default",fn:function(e){return[t._v(" "+t._s(e.row.contact)+" ")]}}])}),n("el-table-column",{attrs:{label:"Post time",align:"center"},scopedSlots:t._u([{key:"default",fn:function(e){return[t._v(" "+t._s(e.row.post_time)+" ")]}}])}),n("el-table-column",{attrs:{label:"Action",align:"center"},scopedSlots:t._u([{key:"default",fn:function(e){return[n("el-dropdown",{attrs:{placement:"bottom",trigger:"click"},on:{command:t.handleCommand}},[n("span",{staticClass:"el-dropdown-link"},[n("i",{staticClass:"el-icon-more",staticStyle:{cursor:"pointer"}})]),n("el-dropdown-menu",{attrs:{slot:"dropdown"},slot:"dropdown"},[n("el-dropdown-item",{attrs:{command:t.beforeHandleCommand(e,"i")}},[n("i",{staticClass:"el-icon-info",staticStyle:{cursor:"pointer"}}),t._v("Details")]),n("el-dropdown-item",{attrs:{command:t.beforeHandleCommand(e,"d")}},[n("i",{staticClass:"el-icon-delete",staticStyle:{cursor:"pointer"}}),t._v("Delete")])],1)],1)]}}])})],1),n("el-dialog",{attrs:{title:"Detail",visible:t.isShowingDetail,html:t.detailHtml},on:{"update:visible":function(e){t.isShowingDetail=e}}},[n("p",{domProps:{innerHTML:t._s(t.detailHtml)}})])],1)},a=[],o=n("50fc"),i={filters:{statusFilter:function(t){var e={Chat:"success","Feature request":"gray","Bug report":"danger"};return e[t]}},data:function(){return{isShowingDetail:!1,detailHtml:"",list:null,listLoading:!0}},created:function(){this.fetchData()},methods:{fetchData:function(){var t=this;this.listLoading=!0,Object(o["c"])().then((function(e){t.list=e.data,t.listLoading=!1}))},beforeHandleCommand:function(t,e){return{scope:t,command:e}},handleCommand:function(t){switch(t.command){case"i":this.detailHtml=t.scope.row.detail,this.isShowingDetail=!0;break}}}},s=i,r=n("2877"),c=Object(r["a"])(s,l,a,!1,null,null,null);e["default"]=c.exports}}]);