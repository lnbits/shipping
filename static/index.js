window.PageShipping = {
  template: '#page-shipping',
  delimiters: ['${', '}'],
  data: function () {
    return {
      currencyOptions: ['sat'],
      defaultRegions: [
        'Africa',
        'Asia',
        'Europe',
        'UK/Ireland',
        'North America',
        'South America',
        'Central America',
        'Caribbean',
        'Oceania',
        'Middle East',
        'Antarctica'
      ],
      settingsFormDialog: {
        show: false,
        data: {
          available_regions: []
        }
      },

      regionsFormDialog: {
        show: false,
        data: {
          name: null,
          regions: [],
          price: null,
          weight_threshold: null,
          price_per_g: null
        }
      },
      regionsList: [],
      regionsTable: {
        search: '',
        loading: false,
        columns: [
          {
            name: 'name',
            align: 'left',
            label: 'Name',
            field: 'name',
            sortable: true
          },
          {
            name: 'regions',
            align: 'left',
            label: 'Regions',
            field: 'regions',
            sortable: true
          },
          {
            name: 'price',
            align: 'left',
            label: 'Price',
            field: 'price',
            sortable: true
          },
          {
            name: 'weight_threshold',
            align: 'left',
            label: 'Weight threshold in grams',
            field: 'weight_threshold',
            sortable: true
          },
          {
            name: 'price_per_g',
            align: 'left',
            label: 'Price per gram',
            field: 'price_per_g',
            sortable: true
          },
          {
            name: 'updated_at',
            align: 'left',
            label: 'Updated At',
            field: 'updated_at',
            sortable: true
          },
          {name: 'id', align: 'left', label: 'ID', field: 'id', sortable: true}
        ],
        pagination: {
          sortBy: 'updated_at',
          rowsPerPage: 10,
          page: 1,
          descending: true,
          rowsNumber: 10
        }
      },

      methodsFormDialog: {
        show: false,
        data: {
          title: null,
          cost_percentage: 0,
          regions: []
        }
      },
      methodsList: [],
      methodsTable: {
        search: '',
        loading: false,
        columns: [
          {
            name: 'title',
            align: 'left',
            label: 'Title',
            field: 'title',
            sortable: true
          },
          {
            name: 'cost_percentage',
            align: 'left',
            label: 'Cost %',
            field: 'cost_percentage',
            sortable: true
          },
          {
            name: 'regions',
            align: 'left',
            label: 'Regions',
            field: 'regions',
            sortable: true
          },
          {
            name: 'updated_at',
            align: 'left',
            label: 'Updated At',
            field: 'updated_at',
            sortable: true
          },
          {name: 'id', align: 'left', label: 'ID', field: 'id', sortable: true}
        ],
        pagination: {
          sortBy: 'updated_at',
          rowsPerPage: 10,
          page: 1,
          descending: true,
          rowsNumber: 10
        }
      }
    }
  },
  watch: {
    'regionsTable.search': {
      handler() {
        const props = {}
        if (this.regionsTable.search) {
          props['search'] = this.regionsTable.search
        }
        this.getRegions()
      }
    },
    'methodsTable.search': {
      handler() {
        const props = {}
        if (this.methodsTable.search) {
          props['search'] = this.methodsTable.search
        }
        this.getMethods()
      }
    }
  },

  methods: {
    //////////////// Settings ////////////////////////
    async updateSettings() {
      try {
        const data = {...this.settingsFormDialog.data}

        await LNbits.api.request('PUT', '/shipping/api/v1/settings', null, data)
        this.settingsFormDialog.show = false
      } catch (error) {
        LNbits.utils.notifyApiError(error)
      }
    },
    async getSettings() {
      try {
        const {data} = await LNbits.api.request(
          'GET',
          '/shipping/api/v1/settings',
          null
        )
        const availableRegions =
          Array.isArray(data.available_regions) && data.available_regions.length
            ? data.available_regions
            : [...this.defaultRegions]
        this.settingsFormDialog.data = {
          ...data,
          available_regions: availableRegions
        }
      } catch (error) {
        LNbits.utils.notifyApiError(error)
      }
    },
    async showSettingsDataForm() {
      await this.getSettings()
      this.settingsFormDialog.show = true
    },

    //////////////// Regions ////////////////////////
    async showNewRegionsForm() {
      this.regionsFormDialog.data = {
        name: null,
        regions: [],
        price: null,
        weight_threshold: null,
        price_per_g: null
      }
      this.regionsFormDialog.show = true
    },
    async showEditRegionsForm(data) {
      this.regionsFormDialog.data = {...data}
      this.regionsFormDialog.show = true
    },
    async saveRegions() {
      try {
        const data = {extra: {}, ...this.regionsFormDialog.data}
        const method = data.id ? 'PUT' : 'POST'
        const entry = data.id ? `/${data.id}` : ''
        await LNbits.api.request(
          method,
          '/shipping/api/v1/regions' + entry,
          null,
          data
        )
        this.getRegions()
        this.regionsFormDialog.show = false
      } catch (error) {
        LNbits.utils.notifyApiError(error)
      }
    },

    async getRegions(props) {
      try {
        this.regionsTable.loading = true
        const params = LNbits.utils.prepareFilterQuery(this.regionsTable, props)
        const {data} = await LNbits.api.request(
          'GET',
          `/shipping/api/v1/regions/paginated?${params}`,
          null
        )
        this.regionsList = data.data
        this.regionsTable.pagination.rowsNumber = data.total
      } catch (error) {
        LNbits.utils.notifyApiError(error)
      } finally {
        this.regionsTable.loading = false
      }
    },
    async deleteRegions(regionsId) {
      await LNbits.utils
        .confirmDialog('Are you sure you want to delete this Regions?')
        .onOk(async () => {
          try {
            await LNbits.api.request(
              'DELETE',
              '/shipping/api/v1/regions/' + regionsId,
              null
            )
            await this.getRegions()
          } catch (error) {
            LNbits.utils.notifyApiError(error)
          }
        })
    },
    async exportRegionsCSV() {
      await LNbits.utils.exportCSV(
        this.regionsTable.columns,
        this.regionsList,
        'regions_' + new Date().toISOString().slice(0, 10) + '.csv'
      )
    },

    //////////////// Methods ////////////////////////
    async showNewMethodForm() {
      this.methodsFormDialog.data = {
        title: null,
        cost_percentage: 0,
        regions: []
      }
      this.methodsFormDialog.show = true
    },
    async showEditMethodForm(data) {
      this.methodsFormDialog.data = {...data}
      this.methodsFormDialog.show = true
    },
    async saveMethod() {
      try {
        const data = {extra: {}, ...this.methodsFormDialog.data}
        const method = data.id ? 'PUT' : 'POST'
        const entry = data.id ? `/${data.id}` : ''
        await LNbits.api.request(
          method,
          '/shipping/api/v1/methods' + entry,
          null,
          data
        )
        this.getMethods()
        this.methodsFormDialog.show = false
      } catch (error) {
        LNbits.utils.notifyApiError(error)
      }
    },

    async getMethods(props) {
      try {
        this.methodsTable.loading = true
        const params = LNbits.utils.prepareFilterQuery(this.methodsTable, props)
        const {data} = await LNbits.api.request(
          'GET',
          `/shipping/api/v1/methods/paginated?${params}`,
          null
        )
        this.methodsList = data.data
        this.methodsTable.pagination.rowsNumber = data.total
      } catch (error) {
        LNbits.utils.notifyApiError(error)
      } finally {
        this.methodsTable.loading = false
      }
    },
    async deleteMethod(methodId) {
      await LNbits.utils
        .confirmDialog('Are you sure you want to delete this Method?')
        .onOk(async () => {
          try {
            await LNbits.api.request(
              'DELETE',
              '/shipping/api/v1/methods/' + methodId,
              null
            )
            await this.getMethods()
          } catch (error) {
            LNbits.utils.notifyApiError(error)
          }
        })
    },

    async exportMethodsCSV() {
      await LNbits.utils.exportCSV(
        this.methodsTable.columns,
        this.methodsList,
        'methods_' + new Date().toISOString().slice(0, 10) + '.csv'
      )
    },
    methodRegionsLabel(regionLabels) {
      if (!Array.isArray(regionLabels)) {
        return ''
      }
      return regionLabels.join(', ')
    },

    //////////////// Utils ////////////////////////
    dateFromNow(date) {
      return moment(date).fromNow()
    },
    async fetchCurrencies() {
      try {
        const response = await LNbits.api.request('GET', '/api/v1/currencies')
        this.currencyOptions = ['sat', ...response.data]
      } catch (error) {
        LNbits.utils.notifyApiError(error)
      }
    }
  },
  ///////////////////////////////////////////////////
  //////LIFECYCLE FUNCTIONS RUNNING ON PAGE LOAD/////
  ///////////////////////////////////////////////////
  async created() {
    this.fetchCurrencies()
    await this.getSettings()
    this.getRegions()
    this.getMethods()
  }
}
