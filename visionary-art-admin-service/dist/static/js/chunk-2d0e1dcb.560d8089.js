(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-2d0e1dcb"],{"7bf0":function(e,t,n){"use strict";n.r(t);var l=function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("div",{staticClass:"app-container"},[n("el-table",{directives:[{name:"loading",rawName:"v-loading",value:e.listLoading,expression:"listLoading"}],attrs:{data:e.list,"element-loading-text":"Loading",border:"",fit:"","highlight-current-row":""}},[n("el-table-column",{attrs:{label:"ID",align:"center",width:"95"},scopedSlots:e._u([{key:"default",fn:function(t){return[e._v(" "+e._s(t.row.id)+" ")]}}])}),n("el-table-column",{attrs:{label:"FUID",align:"center"},scopedSlots:e._u([{key:"default",fn:function(t){return[e._v(" "+e._s(t.row.fuid)+" ")]}}])}),n("el-table-column",{attrs:{label:"Model name",align:"center"},scopedSlots:e._u([{key:"default",fn:function(t){return[n("span",[e._v(e._s(t.row.modelname))])]}}])}),n("el-table-column",{attrs:{label:"Type",align:"center"},scopedSlots:e._u([{key:"default",fn:function(t){return[e._v(" "+e._s(t.row.type)+" ")]}}])}),n("el-table-column",{attrs:{label:"Size",align:"center"},scopedSlots:e._u([{key:"default",fn:function(t){return[e._v(" "+e._s(t.row.size)+" ")]}}])}),n("el-table-column",{attrs:{label:"Upload time",align:"center"},scopedSlots:e._u([{key:"default",fn:function(t){return[e._v(" "+e._s(t.row.upload_time)+" ")]}}])}),n("el-table-column",{attrs:{label:"Action",align:"center"},scopedSlots:e._u([{key:"default",fn:function(t){return[n("el-dropdown",{attrs:{placement:"bottom",trigger:"click"},on:{command:e.handleCommand}},[n("span",{staticClass:"el-dropdown-link"},[n("i",{staticClass:"el-icon-more",staticStyle:{cursor:"pointer"}})]),n("el-dropdown-menu",{attrs:{slot:"dropdown"},slot:"dropdown"},[n("el-dropdown-item",{attrs:{command:e.beforeHandleCommand(t,"d")}},[n("i",{staticClass:"el-icon-delete",staticStyle:{cursor:"pointer"}}),e._v("Delete")])],1)],1)]}}])})],1)],1)},a=[],o=n("50fc"),i={filters:{statusFilter:function(e){var t={online:"success",offline:"info",banned:"danger"};return t[e]}},data:function(){return{list:null,listLoading:!0}},created:function(){this.fetchData()},methods:{fetchData:function(){var e=this;this.listLoading=!0,Object(o["d"])().then((function(t){e.list=t.data,e.listLoading=!1}))},beforeHandleCommand:function(e,t){return{scope:e,command:t}},handleCommand:function(e){switch(e.command){case"d":console.log("Delete");break}}}},r=i,s=n("2877"),c=Object(s["a"])(r,l,a,!1,null,null,null);t["default"]=c.exports}}]);