(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-2d0cc3d7"],{"4ca3":function(t,e,n){"use strict";n.r(e);var l=function(){var t=this,e=t.$createElement,n=t._self._c||e;return n("div",{staticClass:"app-container"},[n("el-table",{directives:[{name:"loading",rawName:"v-loading",value:t.listLoading,expression:"listLoading"}],attrs:{data:t.list,"element-loading-text":"Loading",border:"",fit:"","highlight-current-row":""}},[n("el-table-column",{attrs:{label:"ID",align:"center",width:"95"},scopedSlots:t._u([{key:"default",fn:function(e){return[t._v(" "+t._s(e.row.id)+" ")]}}])}),n("el-table-column",{attrs:{label:"FUID",align:"center"},scopedSlots:t._u([{key:"default",fn:function(e){return[t._v(" "+t._s(e.row.fuid)+" ")]}}])}),n("el-table-column",{attrs:{label:"Model name",align:"center"},scopedSlots:t._u([{key:"default",fn:function(e){return[n("span",[t._v(t._s(e.row.modelname))])]}}])}),n("el-table-column",{attrs:{label:"Type",align:"center"},scopedSlots:t._u([{key:"default",fn:function(e){return[t._v(" "+t._s(e.row.type)+" ")]}}])}),n("el-table-column",{attrs:{label:"Size",align:"center"},scopedSlots:t._u([{key:"default",fn:function(e){return[t._v(" "+t._s(e.row.size)+" ")]}}])}),n("el-table-column",{attrs:{label:"Upload time",align:"center"},scopedSlots:t._u([{key:"default",fn:function(e){return[t._v(" "+t._s(e.row.upload_time)+" ")]}}])}),n("el-table-column",{attrs:{label:"Action",align:"center"},scopedSlots:t._u([{key:"default",fn:function(e){return[n("el-dropdown",{attrs:{placement:"bottom",trigger:"click"},on:{command:t.handleCommand}},[n("span",{staticClass:"el-dropdown-link"},[n("i",{staticClass:"el-icon-more",staticStyle:{cursor:"pointer"}})]),n("el-dropdown-menu",{attrs:{slot:"dropdown"},slot:"dropdown"},[n("el-dropdown-item",{attrs:{command:t.beforeHandleCommand(e,"d")}},[n("i",{staticClass:"el-icon-delete",staticStyle:{cursor:"pointer"}}),t._v("Delete")])],1)],1)]}}])})],1)],1)},a=[],o=n("50fc"),i={filters:{statusFilter:function(t){var e={online:"success",offline:"info",banned:"danger"};return e[t]}},data:function(){return{list:null,listLoading:!0}},created:function(){this.fetchData()},methods:{fetchData:function(){var t=this;this.listLoading=!0,Object(o["d"])().then((function(e){t.list=e.data,t.listLoading=!1}))},beforeHandleCommand:function(t,e){return{scope:t,command:e}},handleCommand:function(t){var e=this;switch(t.command){case"d":Object(o["i"])({id:t.scope.row.id}).then((function(t){e.fetchData()}));break}}}},r=i,s=n("2877"),c=Object(s["a"])(r,l,a,!1,null,null,null);e["default"]=c.exports}}]);