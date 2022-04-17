### implement custom action 
    - action use for bulk operation (issue multiple database command in on go)
    - signature of action method 
        @admin.action(description="action_name")
        def action_method_name(self, request, queryset):
            """
                queryset contain all selected list item 
                use self.message_user() to inform user from 
                result of action
            """