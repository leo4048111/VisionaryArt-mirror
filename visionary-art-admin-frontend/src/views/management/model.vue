<template>
  <div class="app-container">
    <el-table v-loading="listLoading" :data="list" element-loading-text="Loading" border fit highlight-current-row>
      <el-table-column label="ID" align="center" width="95">
        <template slot-scope="scope">
          {{ scope.row.id }}
        </template>
      </el-table-column>
      <el-table-column label="FUID" align="center">
        <template slot-scope="scope">
          {{ scope.row.fuid }}
        </template>
      </el-table-column>
      <el-table-column label="Model name" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.modelname }}</span>
        </template>
      </el-table-column>
      <el-table-column label="Type" align="center">
        <template slot-scope="scope">
          {{ scope.row.type }}
        </template>
      </el-table-column>
      <el-table-column label="Size" align="center">
        <template slot-scope="scope">
          {{ scope.row.size }}
        </template>
      </el-table-column>
      <el-table-column label="Upload time" align="center">
        <template slot-scope="scope">
          {{ scope.row.upload_time }}
        </template>
      </el-table-column>
      <el-table-column label="Action" align="center">
        <template slot-scope="scope">
          <el-dropdown placement="bottom" trigger="click" @command="handleCommand">
            <span class="el-dropdown-link">
              <i class="el-icon-more" style="cursor: pointer;" />
            </span>
            <el-dropdown-menu slot="dropdown">
              <el-dropdown-item :command="beforeHandleCommand(scope, 'd')">
                <i class="el-icon-delete" style="cursor: pointer;" />Delete</el-dropdown-item>
            </el-dropdown-menu>
          </el-dropdown>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
import { getAllModels, removeModel } from '@/api/admin'

export default {
  filters: {
    statusFilter(status) {
      const statusMap = {
        online: 'success',
        offline: 'info',
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
      getAllModels().then(response => {
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
        case 'd':
          removeModel({ id: command.scope.row.id }).then(response => {
            this.fetchData()
          })
          break
      }
    }
  }
}
</script>
