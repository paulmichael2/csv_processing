class TestSanitizeSpecialCharacters:
    def test_sanitize_special_chars(self):
        """Test that special characters including @ are removed from non-email text"""
        test_data = {'Text': ['Hello@World!', 'Test#123$', 'Normal']}
        df = pd.DataFrame(test_data)
        
        result = sanitize_special_characters(df)
        # @ and ! should be removed from non-email columns
        assert result['Text'][0] == 'HelloWorld'
        assert result['Text'][1] == 'Test123'
        assert result['Text'][2] == 'Normal'
    
    def test_exclude_columns(self):
        """Test that excluded columns are NOT sanitized at all"""
        test_data = {
            'Name': ['John@Doe', 'Jane#Smith'],
            'Email': ['john@email.com', 'jane@email.com']
        }
        df = pd.DataFrame(test_data)
        
        result = sanitize_special_characters(df, exclude_cols=['Email'])
        # Name column (not excluded): @ and # removed
        assert result['Name'][0] == 'JohnDoe'
        assert result['Name'][1] == 'JaneSmith'
        # Email column (excluded): kept exactly as-is
        assert result['Email'][0] == 'john@email.com'
        assert result['Email'][1] == 'jane@email.com'
    
    def test_email_columns_keep_at_symbol(self):
        """Test that email columns (not excluded) keep @ symbol"""
        test_data = {
            'user_email': ['john!!!@email.com', 'jane###@test.org'],
            'name': ['John!!!', 'Jane###']
        }
        df = pd.DataFrame(test_data)
        
        result = sanitize_special_characters(df)
        # Email column: !!! and ### removed, but @ and . kept
        assert result['user_email'][0] == 'john@email.com'
        assert result['user_email'][1] == 'jane@test.org'
        # Name column: !!! and ### removed, @ would be removed if present
        assert result['name'][0] == 'John'
        assert result['name'][1] == 'Jane'
    
    def test_preserve_basic_punctuation(self):
        """Test that basic punctuation (., _, -) is preserved in all columns"""
        test_data = {'Text': ['Hello, World!', 'file_name.txt', 'test-value']}
        df = pd.DataFrame(test_data)
        
        result = sanitize_special_characters(df)
        # Comma and ! removed, but . and - kept
        assert 'Hello' in result['Text'][0]
        assert 'World' in result['Text'][0]
        assert result['Text'][1] == 'file_name.txt'
        assert result['Text'][2] == 'test-value'
    
    def test_sanitize_column_names(self):
        """Test that column names (headers) are also sanitized"""
        test_data = {'department!!!': ['Engineering'], 'name': ['John!!!']}
        df = pd.DataFrame(test_data)
        
        result = sanitize_special_characters(df)
        # Column name sanitized
        assert 'department!!!' not in result.columns
        assert 'department' in result.columns
        # Cell value sanitized
        assert '!!!' not in result['name'][0]