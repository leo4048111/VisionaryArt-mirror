<template>
  <div class="app-container">
    <el-table v-loading="listLoading" :data="list" element-loading-text="Loading" border fit highlight-current-row>
      <el-table-column label="ID" align="center" width="95">
        <template slot-scope="scope">
          {{ scope.row.id }}
        </template>
      </el-table-column>
      <el-table-column label="Sender UID" align="center">
        <template slot-scope="scope">
          {{ scope.row.uid }}
        </template>
      </el-table-column>
      <el-table-column label="Title" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.title }}</span>
        </template>
      </el-table-column>
      <el-table-column class-name="status-col" label="Tag" align="center">
        <template slot-scope="scope">
          <el-tag :type="scope.row.tag | statusFilter">{{ scope.row.tag }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="Contact" align="center">
        <template slot-scope="scope">
          {{ scope.row.contact }}
        </template>
      </el-table-column>
      <el-table-column label="Post time" align="center">
        <template slot-scope="scope">
          {{ scope.row.post_time }}
        </template>
      </el-table-column>
      <el-table-column label="Action" align="center">
        <template slot-scope="scope">
          <el-dropdown placement="bottom" trigger="click" @command="handleCommand">
            <span class="el-dropdown-link">
              <i class="el-icon-more" style="cursor: pointer;" />
            </span>
            <el-dropdown-menu slot="dropdown">
              <el-dropdown-item :command="beforeHandleCommand(scope, 'i')">
                <i class="el-icon-info" style="cursor: pointer;" />Details</el-dropdown-item>
              <el-dropdown-item :command="beforeHandleCommand(scope, 'd')">
                <i class="el-icon-delete" style="cursor: pointer;" />Delete</el-dropdown-item>
            </el-dropdown-menu>
          </el-dropdown>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog title="Detail" :visible.sync="isShowingDetail" :html="detailHtml">
      <p v-html="detailHtml" />
    </el-dialog>
  </div>
</template>

<script>
import { getAllFeedbacks } from '@/api/admin'

export default {
  filters: {
    statusFilter(status) {
      const statusMap = {
        'Chat': 'success',
        'Feature request': 'gray',
        'Bug report': 'danger'
      }
      return statusMap[status]
    }
  },
  data() {
    return {
      isShowingDetail: false,
      detailHtml: '',
      list: null,
      listLoading: true
    }
  },
  created() {
    this.fetchData()
  },
  methods: {
    fetchData() {
      this.listLoading = true
      getAllFeedbacks().then(response => {
        this.list = response.data
        this.listLoading = false
      })
    },
    beforeHandleCommand(scope, command) {
      return {
        scope: scope,
        command: command
      }
    },
    handleCommand(command) {
      switch (command.command) {
        case 'i':
          this.detailHtml = command.scope.row.detail
          this.isShowingDetail = true
          break
      }
    }
  }
}
</script>
