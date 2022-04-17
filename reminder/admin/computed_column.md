### create custom or computed column 
    - 1- define a function in this signature
        def method_name(self, instance):
            return 'whatever valid for your condition'
    - 2- then add "method_name" to [list_display] field        