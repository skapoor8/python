class Solution:
    def generate(self, numRows: int) -> List[List[int]]:
        return self.generate_itr(numRows)

    def generate_rec(self, numRows: int) -> List[List[int]]:
        if numRows == 1:
            return [[1]]
        else:
            pascal = self.generate_rec(numRows-1)
            prev_row = pascal[-1]
            cur_row = [1] * numRows
            for i in range(1, numRows-1):
                cur_row[i] = prev_row[i-1] + prev_row[i]
            pascal.append(cur_row)
            return pascal

    def generate_itr_naive(self, numRows: int) -> List[List[int]]:
        pascal = []

        for i in range (1, numRows+1):
            if i == 1:
                pascal.append([1])
            elif i == 2:
                pascal.append([1,1])
            else:
                prev_row = pascal[-1]
                cur_row = [1] * i
                for j in range(1, i-1):
                    cur_row[j] = prev_row[j-1] + prev_row[j]
                pascal.append(cur_row)
        
        return pascal
    
    def generate_itr(self, numRows: int) -> List[List[int]]:
        """
            88-77 solution
        """
        pascal = [ [1] * n for n in range(1, numRows+1) ]

        for r in range (2, numRows):
            for c in range(1, r):
                pascal[r][c] = pascal[r-1][c-1] + pascal[r-1][c]
        
        return pascal