<template id="page-shipping">
  <div class="row q-col-gutter-md">
    <div class="col-12 col-md-8 col-lg-7 q-gutter-y-md">
      <q-card id="settingsCard">
        <q-card-section class="">
          <div class="row">
            <div class="col">
              <span class="text-h5">Shipping</span>
              <q-btn
                @click="showSettingsDataForm()"
                v-if="true"
                unelevated
                split
                color="primary"
                icon="settings"
                class="float-right"
              >
              </q-btn>
            </div>
          </div>
        </q-card-section>
      </q-card>

      <div class="q-mt-lg">
        <span class="text-h5">Regions</span>
      </div>
      <q-card id="regionsCard" class="q-mt-xs">
        <q-card-section class="">
          <div class="row items-center no-wrap q-mb-md">
            <div class="col">
              <q-input
                :label="$t('search')"
                dense
                class="q-pr-xl"
                v-model="regionsTable.search"
              >
                <template v-slot:before>
                  <q-icon name="search"> </q-icon>
                </template>
                <template v-slot:append>
                  <q-icon
                    v-if="regionsTable.search !== ''"
                    name="close"
                    @click="regionsTable.search = ''"
                    class="cursor-pointer"
                  >
                  </q-icon>
                </template>
              </q-input>
            </div>
            <div class="col-auto">
              <q-btn
                @click="showNewRegionsForm()"
                unelevated
                split
                color="primary"
              >
                New Regions
              </q-btn>

              <q-btn
                flat
                color="grey"
                icon="file_download"
                @click="exportRegionsCSV"
                >CSV</q-btn
              >
            </div>
          </div>
          <q-table
            dense
            flat
            :rows="regionsList"
            row-key="id"
            :columns="regionsTable.columns"
            v-model:pagination="regionsTable.pagination"
            :loading="regionsTable.loading"
            @request="getRegions"
          >
            <template v-slot:header="props">
              <q-tr :props="props">
                <q-th auto-width></q-th>
                <q-th v-for="col in props.cols" :key="col.name" :props="props">
                  ${ col.label }
                </q-th>
              </q-tr>
            </template>

            <template v-slot:body="props">
              <q-tr :props="props">
                <q-td auto-width>
                  <q-btn
                    flat
                    dense
                    size="xs"
                    @click="showEditRegionsForm(props.row)"
                    icon="edit"
                    color="light-blue"
                    class="q-mr-sm"
                  >
                    <q-tooltip> Edit </q-tooltip>
                  </q-btn>

                  <q-btn
                    flat
                    dense
                    size="xs"
                    @click="deleteRegions(props.row.id)"
                    icon="cancel"
                    color="pink"
                    class="q-mr-sm"
                  >
                    <q-tooltip> Delete </q-tooltip>
                  </q-btn>
                </q-td>

                <q-td v-for="col in props.cols" :key="col.name" :props="props">
                  <div v-if="col.field == 'updated_at'">
                    <span v-text="dateFromNow(col.value)"> </span>
                  </div>
                  <div
                    v-else-if="
                      Array.isArray(col.value) && col.field == 'regions'
                    "
                  >
                    ${ methodRegionsLabel(col.value) }
                  </div>
                  <div v-else-if="Array.isArray(col.value)">
                    ${ col.value.join(', ') }
                  </div>
                  <div v-else>${ col.value }</div>
                </q-td>
              </q-tr>
            </template>
          </q-table>
        </q-card-section>
      </q-card>

      <div class="q-mt-lg">
        <span class="text-h5">Methods</span>
      </div>
      <q-card id="methodsCard" class="q-mt-xs">
        <q-card-section class="">
          <div class="row items-center no-wrap q-mb-md">
            <div class="col">
              <q-input
                :label="$t('search')"
                dense
                class="q-pr-xl"
                v-model="methodsTable.search"
              >
                <template v-slot:before>
                  <q-icon name="search"> </q-icon>
                </template>
                <template v-slot:append>
                  <q-icon
                    v-if="methodsTable.search !== ''"
                    name="close"
                    @click="methodsTable.search = ''"
                    class="cursor-pointer"
                  >
                  </q-icon>
                </template>
              </q-input>
            </div>
            <div class="col-auto">
              <q-btn
                @click="showNewMethodForm()"
                unelevated
                split
                color="primary"
                class="q-mb-md"
              >
                New Method
              </q-btn>
              <q-btn
                flat
                color="grey"
                icon="file_download"
                class="q-mb-md"
                @click="exportMethodsCSV"
                >CSV</q-btn
              >
            </div>
          </div>
          <q-table
            dense
            flat
            :rows="methodsList"
            row-key="id"
            :columns="methodsTable.columns"
            v-model:pagination="methodsTable.pagination"
            :loading="methodsTable.loading"
            @request="getMethods"
          >
            <template v-slot:header="props">
              <q-tr :props="props">
                <q-th auto-width></q-th>
                <q-th v-for="col in props.cols" :key="col.name" :props="props">
                  ${ col.label }
                </q-th>
              </q-tr>
            </template>

            <template v-slot:body="props">
              <q-tr :props="props">
                <q-td auto-width>
                  <q-btn
                    flat
                    dense
                    size="xs"
                    @click="showEditMethodForm(props.row)"
                    icon="edit"
                    color="light-blue"
                    class="q-mr-sm"
                  >
                    <q-tooltip> Edit </q-tooltip>
                  </q-btn>

                  <q-btn
                    flat
                    dense
                    size="xs"
                    @click="deleteMethod(props.row.id)"
                    icon="cancel"
                    color="pink"
                    class="q-mr-sm"
                  >
                    <q-tooltip> Delete </q-tooltip>
                  </q-btn>
                </q-td>

                <q-td v-for="col in props.cols" :key="col.name" :props="props">
                  <div v-if="col.field == 'updated_at'">
                    <span v-text="dateFromNow(col.value)"> </span>
                  </div>
                  <div v-else-if="Array.isArray(col.value)">
                    ${ col.value.join(', ') }
                  </div>
                  <div v-else>${ col.value }</div>
                </q-td>
              </q-tr>
            </template>
          </q-table>
        </q-card-section>
      </q-card>
    </div>

    <div class="col-12 col-md-4 col-lg-5 q-gutter-y-md">
      <q-card>
        <q-card-section>
          <h6 class="text-subtitle1 q-my-none">Shipping</h6>
          <p>Add shipping to webshop and other extensions</p>
        </q-card-section>
        <q-card-section class="q-pa-none">
          <q-separator></q-separator>
          <q-list>
            <!-- {% include "shipping/_api_docs.html" %} -->
            <q-separator></q-separator>
            <q-expansion-item group="extras" icon="info" label="More info">
              <q-card>
                <q-card-section>
                  <p>Some more info about Shipping.</p>
                  <small
                    >Created by
                    <a
                      class="text-secondary"
                      href="https://github.com/lnbits"
                      target="_blank"
                      >LNbits extension builder</a
                    >.</small
                  >
                </q-card-section>
              </q-card>
            </q-expansion-item>
          </q-list>
        </q-card-section>
      </q-card>
    </div>

    <!--/////////////////////////////////////////////////-->
    <!--//////////////FORM DIALOG////////////////////////-->
    <!--/////////////////////////////////////////////////-->

    <q-dialog v-model="settingsFormDialog.show" position="top">
      <q-card
        v-if="settingsFormDialog.show"
        class="q-pa-lg q-pt-xl lnbits__dialog-card q-col-gutter-md"
      >
        <span class="text-h5">Settings</span>

        <q-select
          filled
          dense
          v-model="settingsFormDialog.data.currency"
          label="currency"
          hint=" "
          :options="currencyOptions"
        ></q-select>

        <q-select
          filled
          dense
          multiple
          use-chips
          v-model="settingsFormDialog.data.available_regions"
          label="Available Regions"
          hint="Select available regions"
          :options="defaultRegions"
        ></q-select>

        <div class="row q-mt-lg">
          <q-btn
            @click="updateSettings"
            unelevated
            color="primary"
            type="submit"
            >Update</q-btn
          >
          <q-btn v-close-popup flat color="grey" class="q-ml-auto"
            >Cancel</q-btn
          >
        </div>
      </q-card>
    </q-dialog>

    <q-dialog v-model="regionsFormDialog.show" position="top">
      <q-card
        v-if="regionsFormDialog.show"
        class="q-pa-lg q-pt-md lnbits__dialog-card q-col-gutter-md"
      >
        <span class="text-h5">Regions</span>

        <q-input
          filled
          dense
          v-model.trim="regionsFormDialog.data.name"
          label="Name"
          hint=" "
        ></q-input>

        <q-select
          filled
          dense
          multiple
          use-chips
          v-model="regionsFormDialog.data.regions"
          label="Regions"
          hint="Select regions "
          :options="
            settingsFormDialog.data.available_regions &&
            settingsFormDialog.data.available_regions.length
              ? settingsFormDialog.data.available_regions
              : defaultRegions
          "
        ></q-select>

        <q-input
          filled
          dense
          v-model.trim="regionsFormDialog.data.price"
          label="Price"
          hint="Standard price "
          type="number"
        ></q-input>

        <q-input
          filled
          dense
          v-model.trim="regionsFormDialog.data.weight_threshold"
          label="Weight threshold in grams"
          hint="Any order below this threshold will use the standard price  (optional)"
          type="number"
        ></q-input>

        <q-input
          filled
          dense
          v-model.trim="regionsFormDialog.data.price_per_g"
          label="Price per gram"
          hint="Any orders above the standard weight threshold will add calculate additional costs  (optional)"
          type="number"
        ></q-input>

        <div class="row q-mt-lg">
          <q-btn @click="saveRegions" unelevated color="primary">
            <span v-if="regionsFormDialog.data.id">Update</span>
            <span v-else>Create</span>
          </q-btn>
          <q-btn v-close-popup flat color="grey" class="q-ml-auto"
            >Cancel</q-btn
          >
        </div>
      </q-card>
    </q-dialog>

    <q-dialog v-model="methodsFormDialog.show" position="top">
      <q-card
        v-if="methodsFormDialog.show"
        class="q-pa-lg q-pt-md lnbits__dialog-card q-col-gutter-md"
      >
        <span class="text-h5">Method</span>

        <q-input
          filled
          dense
          v-model.trim="methodsFormDialog.data.title"
          label="Title"
          hint="Example: standard, next-day"
        ></q-input>

        <q-input
          filled
          dense
          v-model.number="methodsFormDialog.data.cost_percentage"
          label="Cost percentage"
          hint="Percentage to add to the final cost"
          type="number"
        ></q-input>

        <q-select
          filled
          dense
          multiple
          use-chips
          v-model="methodsFormDialog.data.regions"
          label="Regions"
          hint="Select regions"
          :options="methodRegionOptions()"
          emit-value
          map-options
        ></q-select>

        <div class="row q-mt-lg">
          <q-btn @click="saveMethod" unelevated color="primary">
            <span v-if="methodsFormDialog.data.id">Update</span>
            <span v-else>Create</span>
          </q-btn>
          <q-btn v-close-popup flat color="grey" class="q-ml-auto"
            >Cancel</q-btn
          >
        </div>
      </q-card>
    </q-dialog>
  </div>
</template>
