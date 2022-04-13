<?php

namespace App\Http\Middleware;

use App\Models\Role;
use App\Models\User;
use Closure;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;

class RoleMiddleware
{
    /**
     * Handle an incoming request.
     *
     * @param Request $request
     * @param Closure $next
     * @param array|string ...$roles
     * @return mixed
     */
    public function handle(Request $request, Closure $next, array|string ...$roles)
    {
        if(count($roles) == 0)
        {
            $roles = Role::getBaseArray();
        }
        if(Auth::check() && auth()->user()->checkRole($roles))
        {
            return $next($request);
        }
        else
        {
            return redirect(route('auth'));
        }
        abort(403);
    }
}
