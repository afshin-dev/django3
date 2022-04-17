### Example of custum model admin

    class ModelAdmin(admin.ModelAdmin):
        pass

    admin.site.register(actual_model, model_manager)
    admin.site.register(Model, ModelAdmin)

### customize listing page

    - class field of [list_display] = [tableCol... ]
### Editable in listing page
    - list_editable  = [tableCol...]

### number of item in each page 
    - list_per_page = 20

### Eager loading or preloadin fields on table
    - [list_select_related] = [foreignkeyCol...]
    