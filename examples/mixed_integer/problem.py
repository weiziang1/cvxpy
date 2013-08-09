import cvxpy

class Problem(cvxpy.Problem):
    # Use ADMM to attempt non-convex problem.
    def solve(self, rho=0.5, max_iter=5):
        objective,eq_constr,ineq_constr,dims = self.canonicalize()
        variables = self.variables(objective, eq_constr + ineq_constr)
        noncvx_vars = [obj for (id,obj) in variables if obj.noncvx]
        # Form ADMM problem.
        reg_obj = (rho/2)*sum(v.reg_obj() for v in noncvx_vars)
        p = Problem(Minimize(self.objective.expr + reg_obj), 
                    self.constraints)
        # ADMM loop
        for i in range(max_iter):
            p.solve()
            for var in noncvx_vars:
                var.project()
                var.update()