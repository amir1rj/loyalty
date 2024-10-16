Reward_type = (
    # ('amount', 'Amount'),
    # ('percentage', 'Percentage'),
    ('additional_service', 'Additional Service'),
    ('point', 'Point'),
    # ('amount_on_specific_classroom', 'Amount on Specific Classroom'),
    # ('amount_on_specific_department', 'Amount on Specific Department'),
    # ('amount_on_specific_category', 'Amount on Specific Category'),
    # ('amount_on_specific_work_group', 'Amount on Specific Work Group'),
    # ('percentage_on_specific_classroom', 'Percentage on Specific Classroom'),
    # ('percentage_on_specific_department', 'Percentage on Specific Department'),
    # ('percentage_on_specific_category', 'Percentage on Specific Category'),
    # ('percentage_on_specific_work_group', 'Percentage on Specific Work Group'),
    # ('register_in_specific_classroom', 'Register in Specific Classroom'),
)

point_role_type = (
    ( 'Number of Purchases', (
        ('number_of_purchases', 'Number of Purchases'),
        # ("number_of_purchases_with_specific_classroom", "Number of Classrooms with Specific Classroom"),
        # ("number_of_purchases_with_specific_department", "Number of Classrooms with Specific Department"),
        # ("number_of_purchases_with_specific_category", "Number of Classrooms with Specific Category"),
        # ('number_of_purchases_with_specific_work_group', 'Number of Classrooms with Specific Work Group'),
    )),
    ('Average Score', (
        ('avg_score', 'Average Score'),
        # ('avg_score_in_specific_classroom', 'Average Score in Specific Classroom'),
        # ('avg_score_in_specific_department', 'Average Score in Specific Department'),
        # ('avg_score_in_specific_work_group', 'Average Score in Specific Work Group'),
        # ('avg_score_in_specific_category', 'Average Score in Specific Category'),
    )),
    ('First in Class', (
        ('num_of_first_in_class','Num of First in Class'),
        # ('num_of_first_in_class','Num of First in Class in Specific Classroom'),
        # ('num_of_first_in_class','Num of First in Class in Specific Department'),
        # ('num_of_first_in_class','Num of First in Class in Specific Work Group'),
        # ('num_of_first_in_class_in_specific_category','Num of First in Class in Specific Work Category'),

    )),

)
