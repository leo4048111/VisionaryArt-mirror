<template>
  <div class="app-container">
    <el-table v-loading="listLoading" :data="list" element-loading-text="Loading" border fit highlight-current-row>
      <el-table-column label="UID" align="center" width="95">
        <template slot-scope="scope">
          {{ scope.row.uid }}
        </template>
      </el-table-column>
      <el-table-column label="Name" align="center">
        <template slot-scope="scope">
          {{ scope.row.name }}
        </template>
      </el-table-column>
      <el-table-column label="IP" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.ip }}</span>
        </template>
      </el-table-column>
      <el-table-column label="Regdate" align="center">
        <template slot-scope="scope">
          {{ scope.row.regdate }}
        </template>
      </el-table-column>
      <el-table-column class-name="status-col" label="Status" align="center">
        <template slot-scope="scope">
          <el-tag :type="scope.row.stat | statusFilter">{{ scope.row.stat }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="Action" align="center">
        <template slot-scope="scope">
          <el-dropdown placement="bottom" trigger="click" @command="handleCommand">
            <span class="el-dropdown-link">
              <i class="el-icon-more" style="cursor: pointer;" />
            </span>
            <el-dropdown-menu slot="dropdown">
              <el-dropdown-item :command="beforeHandleCommand(scope, 'a')">
                <i class="el-icon-check" style="cursor: pointer;" />Activate</el-dropdown-item>
              <el-dropdown-item :command="beforeHandleCommand(scope, 'b')">
                <i class="el-icon-close" style="cursor: pointer;" />Ban</el-dropdown-item>
            </el-dropdown-menu>
          </el-dropdown>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
import { getAllUsers, banUser, activateUser } from '@/api/admin'

export default {
  filters: {
    statusFilter(status) {
      const statusMap = {
        online: 'success',
        offline: 'gray',
        banned: 'danger'
      }
      return statusMap[status]
    }
  },
  data() {
    return {
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
      getAllUsers().then(response => {
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
        case 'a':
          activateUser({ uid: command.scope.row.uid }).then(response => {
            this.fetchData()
          })
          break
        case 'b':
          banUser({ uid: command.scope.row.uid }).then(response => {
            this.fetchData()
          })
          break
      }
    }
  }
}
</script>
