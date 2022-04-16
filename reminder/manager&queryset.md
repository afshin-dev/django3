### retrieving object 
    - [model].objects.all() 
    - [model].objects.get(pk=?)

### filtering objects
    - [model].objects.filter(col_name=?)    
    - [model].objects.filter(col_name__gt=?)
        - django lookup type === __gt __gte __lt __lte
### Q object 
    - from django.db.modles mport Q
        -- Q | Q => use for or operation
        -- Q $ Q => use for and operation
        -- ~Q negate a Q object 
### reference to a table column 
    - from django.db.models import F 
    - F(col_name)   F(price)
        - in F object we can reference to col of table 
          and relational column 

### sorting data 
    - [model].objects.orderby(*col_names)
    - [model].objects.orderby('title')
    - [model].objects.orderby('title', 'price')
        -- orderby Returns a queryset object
### sorting related method 
    - [models].objects.earliest('title') => sort by title in ASC and give first match    
    - [models].objects.latest('title') => sort by title in DES and give first match              

### limiting result of query 
    -  [model].objects.all()[start:end]

### select column in query
    - [model].objects.all().values(*columns)  Returns dict 
    - [model].objects.all().values_list(*columns)  Returns tuple
    - [model].objects.all().values('id', 'price')


### deffering query
### both method is costly method if not carefully used
    - [model].objects.all().only(*columns) Returns model object
        - if refer to column or property that not exists in *columns arguments
        model object issues extra query for it
    - [model].objects.all().defer(*columns) Returns model object 
        - if refer to column you specify in *columns 
        model object issues extra query 

### select relating (table|object|model)
    ----------------- for one to many relation --------------------------
    ----------------- or foreignkey -------------------------------------
    - [model].objects.select_related(foreingkey).all() Return model object 
    - with preloaded related object (join used for it)

    ----------------- for many to many relation -----------------------
    - [model].objects.prefetch_related(mm_to_m field).all Return model object  

### aggregatin 
    ----------------- from django.db.models.aggregate import Min, Max
    - [model].objects.aggregate(Max('price'))         

### annotate field (query)
    from django.db.models import Value , F , Q
    - [model].objects.annotate(new=Value('new id'))

### calling function (db function)    
    ------- from django.db.models import Func , Value , F
    - [models].objects.annotate(Func(*columns, function='db_function_name'))
    